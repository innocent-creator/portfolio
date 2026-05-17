(() => {
  const canvas = document.getElementById('particles');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let particles = [];
  let animId;
  let mouse = { x: null, y: null };

  const CONFIG = {
    count: 60,
    maxRadius: 2.5,
    minRadius: 0.5,
    speed: 0.4,
    connectionDist: 130,
    mouseRepelDist: 120,
    colors: ['#6c63ff', '#00d4ff', '#8075ff', '#44aaff'],
  };

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };

  class Particle {
    constructor() { this.reset(true); }

    reset(random = false) {
      this.x = random ? Math.random() * canvas.width : Math.random() < 0.5 ? -5 : canvas.width + 5;
      this.y = Math.random() * canvas.height;
      this.r = CONFIG.minRadius + Math.random() * (CONFIG.maxRadius - CONFIG.minRadius);
      this.color = CONFIG.colors[Math.floor(Math.random() * CONFIG.colors.length)];
      this.vx = (Math.random() - 0.5) * CONFIG.speed * 2;
      this.vy = (Math.random() - 0.5) * CONFIG.speed * 2;
      this.alpha = 0.2 + Math.random() * 0.5;
    }

    update() {
      if (mouse.x !== null) {
        const dx = this.x - mouse.x;
        const dy = this.y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONFIG.mouseRepelDist) {
          const force = (CONFIG.mouseRepelDist - dist) / CONFIG.mouseRepelDist;
          this.vx += (dx / dist) * force * 0.8;
          this.vy += (dy / dist) * force * 0.8;
        }
      }

      this.vx *= 0.98;
      this.vy *= 0.98;

      const maxV = CONFIG.speed * 3;
      this.vx = Math.max(-maxV, Math.min(maxV, this.vx));
      this.vy = Math.max(-maxV, Math.min(maxV, this.vy));

      this.x += this.vx;
      this.y += this.vy;

      if (this.x < -20 || this.x > canvas.width + 20 || this.y < -20 || this.y > canvas.height + 20) {
        this.reset();
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.globalAlpha = this.alpha;
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  const init = () => {
    resize();
    particles = Array.from({ length: CONFIG.count }, () => new Particle());
  };

  const drawConnections = () => {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONFIG.connectionDist) {
          const alpha = (1 - dist / CONFIG.connectionDist) * 0.25;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(108, 99, 255, ${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
  };

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawConnections();
    particles.forEach(p => { p.update(); p.draw(); });
    animId = requestAnimationFrame(animate);
  };

  init();
  animate();

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { resize(); }, 200);
  });

  window.addEventListener('mousemove', e => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
  });

  const hero = document.getElementById('hero');
  if (hero) {
    const obs = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) {
        cancelAnimationFrame(animId);
      } else {
        animId = requestAnimationFrame(animate);
      }
    }, { threshold: 0 });
    obs.observe(hero);
  }
})();
