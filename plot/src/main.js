import { getPlotter } from './utils.js';
const indexDiv = document.getElementById('iteration');
const plotters = [
    await getPlotter(['./data/rastrigin.json', './data/rastrigin_gd.json'], 'plot1', 'rastrigin', 'surface'),
    await getPlotter(['./data/rastrigin.json', './data/rastrigin_gd.json'], 'plot2', 'rastrigin', 'contour')
];
let i = 0;
const animate = async () => {
    indexDiv.innerHTML = `${i}`;
    let isDone = false;
    for (const plotter of plotters) {
        isDone = await plotter.update();
    }
    if (!isDone) {
        window.requestAnimationFrame(animate);
        i += 1;
    }
};
window.requestAnimationFrame(animate);
