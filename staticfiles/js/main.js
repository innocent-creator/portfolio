/* ============================================================
   PORTFOLIO MAIN JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ----- LOADER -----
  const loader = document.getElementById('loader');
  document.body.classList.add('loading');
  window.addEventListener('load', () => {
    setTimeout(() => {
      loader.classList.add('hidden');
      document.body.classList.remove('loading');
    }, 600);
  });

  // ----- AOS -----
  AOS.init({
    duration: 700,
    easing: 'ease-out-cubic',
    once: true,
    offset: 60,
  });

  // ----- THEME TOGGLE -----
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = themeToggle?.querySelector('.theme-icon');
  const html = document.documentElement;

  const savedTheme = localStorage.getItem('theme') || 'dark';
  html.setAttribute('data-theme', savedTheme);
  if (themeIcon) themeIcon.textContent = savedTheme === 'dark' ? '🌙' : '☀️';

  themeToggle?.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    if (themeIcon) themeIcon.textContent = next === 'dark' ? '🌙' : '☀️';
  });

  // ----- NAVBAR SCROLL -----
  const navbar = document.getElementById('navbar');
  const backToTop = document.getElementById('backToTop');

  const onScroll = () => {
    const scrollY = window.scrollY;
    navbar?.classList.toggle('scrolled', scrollY > 20);
    backToTop?.classList.toggle('visible', scrollY > 400);
    highlightNavLink();
  };

  window.addEventListener('scroll', onScroll, { passive: true });

  // ----- HAMBURGER -----
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');

  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinks?.classList.toggle('open');
  });

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      hamburger?.classList.remove('open');
      navLinks?.classList.remove('open');
    });
  });

  // ----- ACTIVE NAV LINK -----
  const sections = document.querySelectorAll('section[id]');

  function highlightNavLink() {
    const scrollY = window.scrollY + 120;
    let current = '';
    sections.forEach(sec => {
      if (sec.offsetTop <= scrollY) current = sec.id;
    });
    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href')?.replace('#', '');
      link.classList.toggle('active', href === current);
    });
  }

  // ----- TYPED TEXT -----
  const typedEl = document.getElementById('typedText');
  if (typedEl) {
    const words = [
      'Développeur Django',
      'Développeur Fullstack',
      'Architecte API REST',
      'Développeur FastAPI',
      'Passionné du Web',
    ];
    let wIdx = 0, cIdx = 0, deleting = false;

    const type = () => {
      const word = words[wIdx];
      if (!deleting) {
        typedEl.textContent = word.slice(0, ++cIdx);
        if (cIdx === word.length) {
          deleting = true;
          return setTimeout(type, 2200);
        }
      } else {
        typedEl.textContent = word.slice(0, --cIdx);
        if (cIdx === 0) {
          deleting = false;
          wIdx = (wIdx + 1) % words.length;
        }
      }
      setTimeout(type, deleting ? 60 : 95);
    };
    setTimeout(type, 800);
  }

  // ----- SKILL BARS -----
  const skillsSection = document.getElementById('skills');
  if (skillsSection) {
    const animateBars = () => {
      document.querySelectorAll('.skill-bar-fill').forEach(bar => {
        const target = bar.getAttribute('data-width');
        bar.style.width = target + '%';
      });
    };

    const obs = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        animateBars();
        obs.disconnect();
      }
    }, { threshold: 0.1 });
    obs.observe(skillsSection);
  }

  // ----- SKILLS CAROUSEL AUTO-SCROLL (mobile only) -----
  const skillsCarousel = document.querySelector('.skills-categories');
  if (skillsCarousel) {
    const INTERVAL  = 3000;  // ms between cards
    const MOBILE_BP = 768;
    let autoTimer   = null;
    let isPaused    = false;
    let resumeTimer = null;

    const getCards = () => [...skillsCarousel.querySelectorAll('.skill-cat')];

    const cardLeft = (card) => card.offsetLeft - skillsCarousel.offsetLeft;

    const currentIndex = () => {
      const sl = skillsCarousel.scrollLeft;
      let best = 0, bestDist = Infinity;
      getCards().forEach((card, i) => {
        const dist = Math.abs(cardLeft(card) - sl);
        if (dist < bestDist) { bestDist = dist; best = i; }
      });
      return best;
    };

    const goNext = () => {
      const all = getCards();
      if (!all.length) return;
      const next = (currentIndex() + 1) % all.length;
      skillsCarousel.scrollTo({ left: cardLeft(all[next]), behavior: 'smooth' });
    };

    const startCarousel = () => {
      if (window.innerWidth > MOBILE_BP) return;
      clearInterval(autoTimer);
      autoTimer = setInterval(() => { if (!isPaused) goNext(); }, INTERVAL);
    };

    const stopCarousel = () => { clearInterval(autoTimer); autoTimer = null; };

    // Pause while user touches the carousel, resume 3s after finger lifts
    skillsCarousel.addEventListener('touchstart', () => {
      isPaused = true;
      clearTimeout(resumeTimer);
    }, { passive: true });

    skillsCarousel.addEventListener('touchend', () => {
      clearTimeout(resumeTimer);
      resumeTimer = setTimeout(() => { isPaused = false; }, 3000);
    }, { passive: true });

    // Start/stop when viewport is resized
    window.addEventListener('resize', () => {
      window.innerWidth <= MOBILE_BP ? startCarousel() : stopCarousel();
    });

    // Start only when the skills section enters the viewport
    const skillsSec = document.getElementById('skills');
    if (skillsSec) {
      const carouselObs = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting) startCarousel(); else stopCarousel();
      }, { threshold: 0.15 });
      carouselObs.observe(skillsSec);
    }
  }

  // ----- TESTIMONIALS SLIDER -----
  const track = document.getElementById('testimonialsTrack');
  if (track) {
    const cards = track.querySelectorAll('.testimonial-card');
    const dots = document.querySelectorAll('.slider-dots .dot');
    let current = 0;
    let autoTimer;

    const goTo = idx => {
      current = (idx + cards.length) % cards.length;
      track.style.transform = `translateX(calc(-${current * 100}% - ${current * 2}rem))`;
      dots.forEach((d, i) => d.classList.toggle('active', i === current));
    };

    const startAuto = () => {
      clearInterval(autoTimer);
      autoTimer = setInterval(() => goTo(current + 1), 5000);
    };

    document.getElementById('nextBtn')?.addEventListener('click', () => { goTo(current + 1); startAuto(); });
    document.getElementById('prevBtn')?.addEventListener('click', () => { goTo(current - 1); startAuto(); });
    dots.forEach((dot, i) => dot.addEventListener('click', () => { goTo(i); startAuto(); }));

    if (cards.length > 1) startAuto();
  }

  // ----- CONTACT FORM -----
  const form = document.getElementById('contactForm');
  if (form) {
    const alert = document.getElementById('formAlert');
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const submitIcon = document.getElementById('submitIcon');

    const showAlert = (msg, type) => {
      alert.textContent = msg;
      alert.className = `form-alert ${type}`;
    };

    const setField = (name, error) => {
      const input = form.querySelector(`[name="${name}"]`);
      const errEl = document.getElementById(`${name}-error`);
      if (input) input.classList.toggle('error', !!error);
      if (errEl) errEl.textContent = error || '';
    };

    const validate = data => {
      let ok = true;
      if (!data.nom || data.nom.length < 2) {
        setField('nom', 'Le nom doit comporter au moins 2 caractères.');
        ok = false;
      } else setField('nom', '');

      const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!data.email || !emailRe.test(data.email)) {
        setField('email', 'Adresse email invalide.');
        ok = false;
      } else setField('email', '');

      if (!data.message || data.message.length < 10) {
        setField('message', 'Le message doit comporter au moins 10 caractères.');
        ok = false;
      } else setField('message', '');

      return ok;
    };

    form.addEventListener('submit', async e => {
      e.preventDefault();
      alert.className = 'form-alert';

      const data = {
        nom: form.nom.value.trim(),
        email: form.email.value.trim(),
        sujet: form.sujet.value.trim(),
        message: form.message.value.trim(),
      };

      if (!validate(data)) return;

      submitBtn.disabled = true;
      submitText.textContent = 'Envoi en cours...';
      submitIcon.style.animation = 'loader-spin 1s linear infinite';

      try {
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value;
        const res = await fetch('/contact/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || '',
          },
          body: JSON.stringify(data),
        });

        const json = await res.json();

        if (json.success) {
          showAlert('✅ ' + json.message, 'success');
          form.reset();
          ['nom', 'email', 'message'].forEach(f => setField(f, ''));
        } else {
          showAlert('❌ ' + (json.error || 'Une erreur est survenue.'), 'error');
        }
      } catch {
        showAlert('❌ Erreur réseau. Veuillez réessayer.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitText.textContent = 'Envoyer le message';
        submitIcon.style.animation = '';
      }
    });
  }

  // ----- SMOOTH SCROLL for hash links -----
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        const top = target.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

});
