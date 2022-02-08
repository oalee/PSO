import { getPlotter } from './utils.js';
const indexDiv = document.getElementById('iteration');
// const fileName = 'obj_f:rosenbrock,n_par:40,iter:1000,in_srat:DynamicAdaptiveStrategy,rng:100,grd_coef:0,seed:132176,rnd_grad:false'
const fileName = 'obj_f:rosenbrock,n_par:10,iter:40,in_srat:DynamicAdaptiveStrategy,rng:10,grd_coef:0,seed:753786,rnd_grad:false';
const plotters = [
    await getPlotter([`./data/${fileName}.json`,
        `./data/${fileName}_gd.json`], 'plot1', 'rastrigin', 'surface'),
    await getPlotter([`./data/${fileName}.json`, `./data/${fileName}_gd.json`], 'plot2', 'rastrigin', 'contour')
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
