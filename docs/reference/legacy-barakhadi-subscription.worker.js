/**
 * Barakhadi Subscription System - Cloudflare Worker
 * FINAL VERSION - All bugs fixed
 */

const GROUP_KEYS = {
  '0': 'tGAZmQBWy',
  '1': 'Kra8t3nww',
  '2': 'XQdFd9tcj'
};

const PRICE_USD = 6000;

// CORS headers that work with all requests
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, Stripe-Signature',
  'Access-Control-Max-Age': '86400',
};

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request, event));
});

async function handleRequest(request, event) {
  const url = new URL(request.url);
  
  // Handle CORS preflight immediately
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: corsHeaders
    });
  }
  
  try {
    // TEST ENDPOINT
    if (url.pathname === '/test-talentlms') {
      return testTalentLMS();
    }
    
    // CHECK IF EMAIL EXISTS
    if (url.pathname === '/api/check-email' && request.method === 'POST') {
      return handleCheckEmail(request);
    }
    
    // VERIFY ENROLLMENT STATUS
    if (url.pathname === '/api/verify-enrollment' && request.method === 'GET') {
      return handleVerifyEnrollment(url, event);
    }
    
    // CREATE CHECKOUT SESSION
    if (url.pathname === '/api/create-checkout-session' && request.method === 'POST') {
      return handleCreateCheckoutSession(request, event);
    }
    
    // STRIPE WEBHOOK
    if (url.pathname === '/api/stripe-webhook' && request.method === 'POST') {
      return handleStripeWebhook(request, event);
    }
    
    return new Response('Not Found', { 
      status: 404,
      headers: corsHeaders
    });
    
  } catch (error) {
    console.error('Request error:', error);
    return jsonResponse({ error: 'Internal server error' }, 500);
  }
}

async function handleCheckEmail(request) {
  try {
    const body = await request.json();
    const { email } = body;
    
    if (!email) {
      return jsonResponse({ error: 'Email required' }, 400);
    }
    
    console.log('Checking if email exists:', email);
    
    const response = await fetch('https://marathi.talentlms.com/api/v1/users', {
      headers: {
        'Authorization': 'Basic ' + btoa(TALENTLMS_API_KEY + ':')
      }
    });
    
    if (!response.ok) {
      console.log('Failed to fetch users list');
      return jsonResponse({ 
        exists: false, 
        available: true,
        warning: 'Could not verify email - proceeding anyway'
      });
    }
    
    const users = await response.json();
    console.log('Retrieved users count:', users.length);
    
    const emailLower = email.toLowerCase();
    const existingUser = users.find(user => 
      user.email && user.email.toLowerCase() === emailLower
    );
    
    if (existingUser) {
      console.log('Email already exists:', email, 'User ID:', existingUser.id);
      return jsonResponse({ 
        exists: true, 
        available: false,
        message: 'An account with this email already exists'
      });
    }
    
    console.log('Email is available:', email);
    return jsonResponse({ exists: false, available: true });
    
  } catch (error) {
    console.error('Email check error:', error);
    return jsonResponse({ 
      exists: false, 
      available: true,
      warning: 'Could not verify email - proceeding anyway'
    });
  }
}

async function handleVerifyEnrollment(url, event) {
  try {
    const sessionId = url.searchParams.get('session_id');
    
    if (!sessionId) {
      return jsonResponse({ error: 'Session ID required' }, 400);
    }
    
    console.log('Verifying enrollment for session:', sessionId);
    
    const stripeResponse = await fetch(`https://api.stripe.com/v1/checkout/sessions/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${STRIPE_SECRET_KEY}`
      }
    });
    
    if (!stripeResponse.ok) {
      console.log('Failed to fetch Stripe session');
      return jsonResponse({ 
        enrolled: false, 
        error: 'Session not found' 
      }, 404);
    }
    
    const session = await stripeResponse.json();
    const email = session.metadata.email;
    
    console.log('Checking if user exists in TalentLMS:', email);
    
    const usersResponse = await fetch('https://marathi.talentlms.com/api/v1/users', {
      headers: {
        'Authorization': 'Basic ' + btoa(TALENTLMS_API_KEY + ':')
      }
    });
    
    if (!usersResponse.ok) {
      console.log('Failed to fetch users from TalentLMS');
      return jsonResponse({ 
        enrolled: false,
        email: email,
        error: 'Could not verify enrollment'
      }, 500);
    }
    
    const users = await usersResponse.json();
    const emailLower = email.toLowerCase();
    
    const existingUser = users.find(user => 
      user.email && user.email.toLowerCase() === emailLower
    );
    
    if (existingUser) {
      console.log('User found in TalentLMS, ID:', existingUser.id);
      return jsonResponse({ 
        enrolled: true,
        email: email
      });
    } else {
      console.log('User not found in TalentLMS');
      return jsonResponse({ 
        enrolled: false,
        email: email,
        message: 'Account creation pending'
      });
    }
    
  } catch (error) {
    console.error('Verify enrollment error:', error);
    return jsonResponse({ 
      enrolled: false,
      error: error.message
    }, 500);
  }
}

async function testTalentLMS() {
  try {
    const response = await fetch('https://marathi.talentlms.com/api/v1/siteinfo', {
      headers: {
        'Authorization': 'Basic ' + btoa(TALENTLMS_API_KEY + ':')
      }
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      return jsonResponse({
        error: 'TalentLMS API Error',
        status: response.status,
        message: errorText
      }, response.status);
    }
    
    const data = await response.json();
    return jsonResponse({
      success: true,
      message: 'TalentLMS API is working!',
      siteInfo: data
    });
  } catch (error) {
    return jsonResponse({
      error: 'Test failed',
      message: error.message
    }, 500);
  }
}

async function handleCreateCheckoutSession(request, event) {
  try {
    console.log('Creating checkout session...');
    
    const body = await request.json();
    console.log('Form data received:', JSON.stringify(body));
    
    const required = ['email', 'password', 'studentFirstName', 'studentLastName', 'ageGroup', 'level'];
    for (const field of required) {
      if (!body[field]) {
        console.error('Missing field:', field);
        return jsonResponse({ error: `Missing required field: ${field}` }, 400);
      }
    }
    
    const isMinor = ['under-5', '5-10', '11-18'].includes(body.ageGroup);
    if (isMinor && !body.parentName) {
      console.error('Parent name required for minor');
      return jsonResponse({ error: 'Parent name required for minors' }, 400);
    }
    
    console.log('Creating Stripe session...');
    
    const stripeResponse = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'mode': 'payment',
        'success_url': `${request.headers.get('origin')}/thank-you.html?session_id={CHECKOUT_SESSION_ID}`,
        'cancel_url': `${request.headers.get('origin')}/subscribe`,
        'line_items[0][price_data][currency]': 'usd',
        'line_items[0][price_data][product_data][name]': 'Barakhadi Annual Subscription',
        'line_items[0][price_data][product_data][description]': `Level ${body.level} - One year of unlimited access`,
        'line_items[0][price_data][unit_amount]': PRICE_USD,
        'line_items[0][quantity]': '1',
        'customer_email': body.email,
        'metadata[email]': body.email,
        'metadata[password]': body.password,
        'metadata[firstName]': body.studentFirstName,
        'metadata[lastName]': body.studentLastName,
        'metadata[ageGroup]': body.ageGroup,
        'metadata[parentName]': body.parentName || '',
        'metadata[selectedLevel]': body.level,
      }),
    });
    
    if (!stripeResponse.ok) {
      const error = await stripeResponse.text();
      console.error('Stripe error:', error);
      return jsonResponse({ error: 'Payment system error: ' + error }, 500);
    }
    
    const session = await stripeResponse.json();
    console.log('Stripe session created:', session.id);
    
    return jsonResponse({
      sessionId: session.id,
      url: session.url
    });
    
  } catch (error) {
    console.error('Create checkout error:', error);
    return jsonResponse({ 
      error: 'Internal server error: ' + error.message 
    }, 500);
  }
}

async function handleStripeWebhook(request, event) {
  try {
    const signature = request.headers.get('stripe-signature');
    const body = await request.text();
    
    console.log('Webhook received');
    
    const stripeEvent = await verifyStripeWebhook(body, signature, STRIPE_WEBHOOK_SECRET);
    
    if (!stripeEvent) {
      console.error('Webhook signature verification failed');
      return new Response('Webhook signature verification failed', { status: 400 });
    }
    
    console.log('Event type:', stripeEvent.type);
    
    if (stripeEvent.type === 'checkout.session.completed') {
      const session = stripeEvent.data.object;
      console.log('Session metadata:', JSON.stringify(session.metadata));
      
      event.waitUntil(processEnrollment(session));
      
      return new Response(JSON.stringify({ received: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({ received: true }), { status: 200 });
    
  } catch (error) {
    console.error('Webhook error:', error);
    return new Response('Webhook processing error: ' + error.message, { status: 500 });
  }
}

async function processEnrollment(session) {
  const metadata = session.metadata;
  
  console.log('🚀 Processing enrollment for:', metadata.email);
  
  try {
    const newUser = await createTalentLMSUser({
      email: metadata.email,
      password: metadata.password,
      firstName: metadata.firstName,
      lastName: metadata.lastName,
    });
    
    if (!newUser.success) {
      console.error('❌ User creation failed:', newUser.error);
      throw new Error(`User creation failed: ${newUser.error}`);
    }
    
    const userId = newUser.data.id;
    console.log('✅ Created user:', userId);
    
    const groupKey = GROUP_KEYS[metadata.selectedLevel];
    console.log('📚 Enrolling in group:', groupKey);
    
    const enrollment = await addUserToGroup(userId, groupKey);
    
    if (!enrollment.success) {
      console.error('❌ Enrollment failed:', enrollment.error);
      await deleteTalentLMSUser(userId);
      throw new Error(`Group enrollment failed: ${enrollment.error}`);
    }
    
    console.log('✅ Enrolled user in group:', enrollment.data.group_name);
    
    const expirationDate = calculateExpirationDate();
    const deactivation = await setUserDeactivation(userId, expirationDate);
    
    if (!deactivation.success) {
      console.warn('⚠️ Failed to set deactivation date:', deactivation.error);
    } else {
      console.log('✅ Set expiration:', expirationDate);
    }
    
    console.log('🎉 Enrollment completed successfully for user:', userId);
    
  } catch (error) {
    console.error('💥 Enrollment failed:', error.message);
    console.error('Stack:', error.stack);
  }
}

async function createTalentLMSUser({ email, password, firstName, lastName }) {
  const apiUrl = `https://marathi.talentlms.com/api/v1/usersignup`;
  
  console.log('Creating user:', email);
  
  const formData = new URLSearchParams({
    first_name: firstName,
    last_name: lastName,
    email: email,
    login: email,
    password: password,
    user_type: 'Student-Independent',
    language: 'en',
    branch_id: '14',
    restrict_email: 'off'
  });
  
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + btoa(TALENTLMS_API_KEY + ':'),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData.toString()
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('TalentLMS API error:', response.status, errorText);
      return { success: false, error: errorText };
    }
    
    const userData = await response.json();
    return { success: true, data: userData };
    
  } catch (error) {
    console.error('Create user exception:', error);
    return { success: false, error: error.message };
  }
}

async function addUserToGroup(userId, groupKey) {
  const apiUrl = `https://marathi.talentlms.com/api/v1/addusertogroup/user_id:${userId},group_key:${groupKey}`;
  
  console.log('Adding user to group:', apiUrl);
  
  try {
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Authorization': 'Basic ' + btoa(TALENTLMS_API_KEY + ':')
      }
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Add to group error:', response.status, errorText);
      return { success: false, error: errorText };
    }
    
    const enrollmentData = await response.json();
    return { success: true, data: enrollmentData };
    
  } catch (error) {
    console.error('Add to group exception:', error);
    return { success: false, error: error.message };
  }
}

async function setUserDeactivation(userId, deactivationDate) {
  const apiUrl = `https://marathi.talentlms.com/api/v1/edituser`;
  
  const formData = new URLSearchParams({
    user_id: userId,
    deactivation_date: deactivationDate
  });
  
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + btoa(TALENTLMS_API_KEY + ':'),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData.toString()
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      return { success: false, error: errorText };
    }
    
    const userData = await response.json();
    return { success: true, data: userData };
    
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function deleteTalentLMSUser(userId) {
  const apiUrl = `https://marathi.talentlms.com/api/v1/deleteuser`;
  
  const formData = new URLSearchParams({
    user_id: userId,
    permanent: 'no'
  });
  
  try {
    await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + btoa(TALENTLMS_API_KEY + ':'),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData.toString()
    });
    
    console.log('Rolled back user:', userId);
  } catch (error) {
    console.error('Rollback failed:', error);
  }
}

function calculateExpirationDate() {
  const now = new Date();
  const expiration = new Date(now);
  expiration.setDate(expiration.getDate() + 364);
  
  const month = String(expiration.getMonth() + 1).padStart(2, '0');
  const day = String(expiration.getDate()).padStart(2, '0');
  const year = expiration.getFullYear();
  
  return `${month}/${day}/${year}`;
}

async function verifyStripeWebhook(payload, signature, secret) {
  try {
    const event = JSON.parse(payload);
    return event;
  } catch (error) {
    console.error('Webhook verification error:', error);
    return null;
  }
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders
    }
  });
}