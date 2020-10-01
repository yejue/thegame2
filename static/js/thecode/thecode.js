const randomMinMax = (min, max) => {
  return min + Math.random() * (max - min);
};
const button = document.querySelector('.menu-btn');
const menu = document.querySelector('.menu');
const buttonPulse = document.querySelectorAll('.menu-btn-pulse');

const btnHoverTl = new TimelineMax({
  repeat: -1,
  paused: true });

btnHoverTl.fromTo(button, 0.8, {
  scale: 1 },
{
  scale: 1.05 }).

to(button, 0.6, {
  scale: 1 });


const pulseTl = new TimelineMax({
  repeat: -1,
  onRepeat: () => {
    TweenMax.set(buttonPulse, { scale: 0.5 });
  } });


pulseTl.staggerTo(buttonPulse, 2, {
  scale: 2.5,
  transformOrigin: "center center" },
0.25, 'in').
staggerTo(buttonPulse, 2, {
  opacity: 0,
  scale: 3.5 },
0.25, 'in+=0.25');

button.addEventListener('click', () => {
  menu.classList.toggle('active');
  button.classList.toggle('open');
  // play particles on click
  button.classList.contains('open') ? playParticles() : null;

  if (button.classList.contains('open')) {
    pulseTl.eventCallback("onRepeat", () => {
      pulseTl.pause();
    });
    btnHoverTl.eventCallback('onRepeat', () => {
      btnHoverTl.pause();
    });
  } else
  {
    pulseTl.eventCallback("onRepeat", null);
    pulseTl.restart();
    btnHoverTl.eventCallback('onRepeat', null);
    btnHoverTl.restart();
  }
});

button.addEventListener('mouseover', () => {
  btnHoverTl.play();
  btnHoverTl.eventCallback("onRepeat", null);
});

button.addEventListener('mouseleave', () => {
  btnHoverTl.eventCallback("onRepeat", () => {
    btnHoverTl.pause();
  });
});

const colors = ["#F829AB", "#F42977", "#F41F5F"];
const particleCount = 8;
const btnContainer = document.querySelector('.menu-btn-container');

// create a few span elements
const createParticles = () => {
  for (let i = 0; i < particleCount; i++) {
    // create element
    const particle = document.createElement('span');
    // assign class to element
    particle.setAttribute('class', 'menu-btn-particle');
    btnContainer.appendChild(particle);
  }
};

createParticles();

const particle = document.querySelectorAll('.menu-btn-particle');

randomizeParticles = () => {
  let color = colors[Math.random() * colors.length | 0];
  TweenMax.set(particle, { x: 0, y: 0, backgroundColor: () => color });
  TweenMax.set(particle, { scale: () => randomMinMax(0.35, 1) });
  TweenMax.set(particle, { opacity: () => randomMinMax(0.25, 1) });
};

randomizeParticles();


playParticles = () => {
  const particleTl = new TimelineMax();
  particleTl.staggerTo(particle, 0.5, { cycle: {
      physics2D: () => {
        return {
          velocity: randomMinMax(145, 165),
          angle: randomMinMax(180, 325),
          gravity: randomMinMax(215, 225) };

      } } },
  'in').
  to(particle, 0.4, { scale: 0, opacity: 0, onComplete: () => {
      randomizeParticles();
    } }, 'in');
};