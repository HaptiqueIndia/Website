(() => {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  const host = window.location.hostname;
  const isLocalDeveloper = host === 'localhost' || host === '127.0.0.1' || host === '[::1]';
  const isComingSoonPage = page === 'coming-soon.html';

  if (isLocalDeveloper || isComingSoonPage) return;

  window.location.replace(`/coming-soon.html?from=${encodeURIComponent(page)}`);
})();
