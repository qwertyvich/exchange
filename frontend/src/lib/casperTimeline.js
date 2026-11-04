// Seconds: 10 hover, 1.5 exit, 2 hidden, .7 left entrance, 4 peek,
// .5 left exit, 2 hidden, .7 right entrance, 7 peek, 1.5 exit, 4 hidden, 1 return.
export const CASPER_DURATION = 34900;

export function casperTimeline({ home, width, height, headingTop, receiveTop }) {
  const homeScale = home.width / 100;
  const peekSize = Math.min(128, Math.max(88, width * .22));
  const peekScale = peekSize / 100;
  const clampY = y => Math.max(home.y + home.height + 12, Math.min(y, height - peekSize - 12));
  const leftY = clampY(headingTop + 8);
  const rightY = clampY(receiveTop + 4);
  const transform = (x, y, scale, angle = 0) => `translate3d(${x}px, ${y}px, 0) scale(${scale}) translate(50px, 50px) rotate(${angle}deg) translate(-50px, -50px)`;
  const atHome = delta => transform(home.x, home.y + delta, homeScale);
  const offHome = transform(-home.width * 2, home.y - 12, homeScale);
  const leftOff = transform(-peekSize * 1.2, leftY, peekScale, 90);
  const leftPeek = transform(-peekSize * .45, leftY, peekScale, 90);
  const rightOff = transform(width + peekSize * .2, rightY, peekScale, -90);
  const rightPeek = transform(width - peekSize * .55, rightY, peekScale, -90);
  const frame = (time, value, opacity = 1, easing = 'ease-in-out') => ({ offset: time / CASPER_DURATION, transform: value, opacity, easing });
  const hovering = [];
  for (let cycle = 0; cycle < 4; cycle++) {
    for (const [fraction, delta] of [[0, 0], [.25, -3], [.5, 0], [.75, 3]]) {
      hovering.push(frame((cycle + fraction) * 2500, atHome(delta)));
    }
  }
  hovering.push(frame(10000, atHome(0)));
  return {
    body: [
      ...hovering,
      frame(11500, offHome, 0),
      frame(13500, leftOff, 0),
      frame(14200, leftPeek),
      frame(18200, leftPeek),
      frame(18700, leftOff, 0),
      frame(20700, rightOff, 0),
      frame(21400, rightPeek),
      frame(28400, rightPeek),
      frame(29900, rightOff, 0),
      frame(33900, offHome, 0),
      frame(CASPER_DURATION, atHome(0)),
    ],
    accessories: [...hovering, frame(CASPER_DURATION, atHome(0))],
  };
}
