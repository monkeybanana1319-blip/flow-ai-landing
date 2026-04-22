// ============ Fade-in on scroll ============
const io = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('in'), i * 40);
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-up').forEach(el => io.observe(el));

// ============ FAQ accordion ============
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => q.parentElement.classList.toggle('open'));
});

// ============ WhatsApp click tracking ============
// Fires a GA4 'whatsapp_click' event and a Meta Pixel 'Contact' event
// when any <a href="https://wa.me/..."> is clicked. No-op if GA/Pixel not loaded.
document.querySelectorAll('a[href*="wa.me/"]').forEach(a => {
  a.addEventListener('click', () => {
    const label = a.className || a.innerText.trim().slice(0, 40) || 'unknown';
    try { if (typeof gtag === 'function') gtag('event', 'whatsapp_click', { cta: label }); } catch (_) {}
    try { if (typeof fbq === 'function') fbq('track', 'Contact', { cta: label }); } catch (_) {}
  });
});
