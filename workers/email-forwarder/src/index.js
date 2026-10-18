// Forwards mail sent to info@barakhadi.com to every address in FORWARD_TO.
// Cloudflare Email Routing hands each incoming message to this Worker (routing rule: info@ -> "Send to a Worker").
// Every destination must be a verified address under Email Routing -> Destination addresses.
export default {
  async email(message, env) {
    const destinations = String(env.FORWARD_TO ?? '')
      .split(',')
      .map((a) => a.trim())
      .filter(Boolean);

    if (destinations.length === 0) {
      message.setReject('Mailbox not configured');
      return;
    }

    const results = await Promise.allSettled(destinations.map((to) => message.forward(to)));
    results.forEach((r, i) => {
      if (r.status === 'rejected') console.error(`forward to ${destinations[i]} failed:`, r.reason);
    });

    // If every forward failed, bounce so the sender knows; otherwise the mail reached at least one inbox.
    if (results.every((r) => r.status === 'rejected')) {
      message.setReject('Temporary delivery problem, please try again later');
    }
  },
};
