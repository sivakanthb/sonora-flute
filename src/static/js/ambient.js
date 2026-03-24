/* ============================================================
   Sonora — Ambient Floating Background
   Gentle mist, musical notes, and glowing orbs
   that evoke the feeling of listening to a
   soulful flute melody beside a flowing river
   ============================================================ */
(function () {
  'use strict';

  const canvas = document.createElement('canvas');
  canvas.id = 'sonora-ambient';
  Object.assign(canvas.style, {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100vw',
    height: '100vh',
    zIndex: '0',
    pointerEvents: 'none'
  });
  document.body.prepend(canvas);

  const ctx = canvas.getContext('2d');
  let w, h, particles;

  const NOTES = ['\u266A', '\u266B', '\u266C', '\u2669'];

  function isDark() {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  }

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }

  function seed() {
    particles = [];
    var count = Math.min(30, Math.floor((w * h) / 35000));

    for (var i = 0; i < count; i++) {
      var roll = Math.random();

      if (roll < 0.2) {
        // Musical note — drifts upward slowly
        particles.push({
          t: 'n',
          x: Math.random() * w,
          y: Math.random() * h,
          ch: NOTES[Math.floor(Math.random() * NOTES.length)],
          sz: Math.random() * 12 + 10,
          vx: (Math.random() - 0.5) * 0.12,
          vy: -(Math.random() * 0.25 + 0.08),
          a: Math.random() * 0.10 + 0.03,
          rot: Math.random() * Math.PI * 2,
          rs: (Math.random() - 0.5) * 0.003
        });
      } else if (roll < 0.55) {
        // Mist wisp — drifts horizontally with gentle pulse
        particles.push({
          t: 'm',
          x: Math.random() * w,
          y: Math.random() * h,
          r: Math.random() * 100 + 50,
          vx: (Math.random() - 0.5) * 0.15,
          vy: (Math.random() - 0.5) * 0.06,
          a: Math.random() * 0.028 + 0.008,
          ph: Math.random() * Math.PI * 2,
          ps: Math.random() * 0.004 + 0.001
        });
      } else {
        // Soft orb — gentle glow
        var colors = isDark()
          ? ['212,152,94', '90,176,216', '140,170,210']
          : ['200,136,92', '74,144,184', '100,150,200'];
        particles.push({
          t: 'o',
          x: Math.random() * w,
          y: Math.random() * h,
          r: Math.random() * 2 + 0.8,
          vx: (Math.random() - 0.5) * 0.18,
          vy: (Math.random() - 0.5) * 0.12,
          a: Math.random() * 0.22 + 0.06,
          c: colors[Math.floor(Math.random() * colors.length)]
        });
      }
    }
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    var dark = isDark();

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];

      // Move
      p.x += p.vx;
      p.y += p.vy;

      // Wrap around edges with padding
      if (p.x < -150) p.x = w + 150;
      if (p.x > w + 150) p.x = -150;
      if (p.y < -150) p.y = h + 50;
      if (p.y > h + 150) p.y = -150;

      if (p.t === 'n') {
        // Musical note
        p.rot += p.rs;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.font = p.sz + "px 'Playfair Display', Georgia, serif";
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = dark
          ? 'rgba(212,180,130,' + p.a + ')'
          : 'rgba(120,150,180,' + p.a + ')';
        ctx.fillText(p.ch, 0, 0);
        ctx.restore();
      } else if (p.t === 'm') {
        // Mist wisp
        p.ph += p.ps;
        var ma = p.a * (0.6 + 0.4 * Math.sin(p.ph));
        var mc = dark ? '140,180,220' : '130,170,210';
        var g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
        g.addColorStop(0, 'rgba(' + mc + ',' + ma + ')');
        g.addColorStop(1, 'rgba(' + mc + ',0)');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      } else {
        // Soft orb
        var og = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4);
        og.addColorStop(0, 'rgba(' + p.c + ',' + p.a + ')');
        og.addColorStop(1, 'rgba(' + p.c + ',0)');
        ctx.fillStyle = og;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    requestAnimationFrame(draw);
  }

  resize();
  seed();
  draw();

  window.addEventListener('resize', function () {
    resize();
    seed();
  });

  // Re-seed colors when theme changes
  var observer = new MutationObserver(function () { seed(); });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
