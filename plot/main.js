const drawPlot = async () => {
  const objectiveFuntionName = "rastrigin";
  const rawData = await (await fetch(`f_${objectiveFuntionName}.json`)).json();
  const minPositionX = Math.min(
    ...rawData.flatMap((x) => x.map((y) => y.position[0]))
  );
  const minPositionY = Math.min(
    ...rawData.flatMap((x) => x.map((y) => y.position[1]))
  );
  const maxPositionX = Math.max(
    ...rawData.flatMap((x) => x.map((y) => y.position[0]))
  );
  const maxPositionY = Math.max(
    ...rawData.flatMap((x) => x.map((y) => y.position[1]))
  );
  const rastrigin = (x) =>
    x.reduce(
      (acc, val) => acc + Math.pow(val, 2) - 10 * Math.cos(2 * Math.PI * val),
      0
    ) + 20;
  const rosenbrock = (x) => {
    const a = 0;
    const b = 1;
    return Math.pow(a - x[0], 2) + b * Math.pow(x[1] - Math.pow(x[0], 2), 2);
  };
  const objectiveFuntions = {
    rastrigin,
    rosenbrock,
  };
  const chosenFuntion = objectiveFuntions[objectiveFuntionName];
  const z_data = [];
  const pixDensity = 150;
  const xStep = (maxPositionX - minPositionX) / pixDensity;
  const yStep = (maxPositionY - minPositionY) / pixDensity;
  for (let i = 0; i < pixDensity; i++) {
    const row = [];
    for (let j = 0; j < pixDensity; j++) {
      const x = minPositionX + xStep * i;
      const y = minPositionY + yStep * j;
      row.push(chosenFuntion([x, y]));
    }
    z_data.push(row);
  }
  const min = Math.min(...z_data.flatMap((r) => r));
  const max = Math.max(...z_data.flatMap((r) => r));
  const normalizeZ = (y) => (y - min) / (max - min);
  const fixedZData = z_data.map((x) => x.map(normalizeZ));
  const trace1 = {
    z: fixedZData,
    type: "surface",
  };

  /*
	 {
      x: 2,
      y: 5,
      xref: 'x',
      yref: 'y',
      text: 'Annotation Text',
      showarrow: true,
      arrowhead: 7,
      ax: 0k,
      ay: -40
    }

		var trace1 = {
	x:unpack(rows, 'x1'), y: unpack(rows, 'y1'), z: unpack(rows, 'z1'),
	mode: 'markers',
	marker: {
		size: 12,
		line: {
		color: 'rgba(217, 217, 217, 0.14)',
		width: 0.5},
		opacity: 0.8},
	type: 'scatter3d'
};
		*/

  const ballShift = (max - min) / 45;
  const normalizeX = (x) => (x - minPositionX) / (maxPositionX - minPositionX);
  const normalizeY = (x) => (x - minPositionY) / (maxPositionY - minPositionY);
  const trace2 = {
    x: rawData[0].map((p) => pixDensity * normalizeY(p.position[1])),
    y: rawData[0].map((p) => pixDensity * normalizeX(p.position[0])),
    z: rawData[0].map((p) => normalizeZ(chosenFuntion(p.position)) + ballShift),
    mode: "markers",
    marker: {
      size: 4,
      line: {
        color: "rgba(217, 217, 217, 0.14)",
        width: 0.5,
      },
      opacity: 0.8,
    },
    type: "scatter3d",
  };
  const data = [trace1, trace2];
  const layout = {
    title: objectiveFuntionName,
    autosize: true,
    width: window.innerWidth,
    height: window.innerHeight,
    scene: {
      camera: {
        eye:
          objectiveFuntionName === "rastrigin"
            ? { x: 0.8, y: -0.8, z: 1.5 }
            : {},
      },
    },
    margin: {
      l: 65,
      r: 50,
      b: 65,
      t: 90,
    },
  };
  const plot = document.getElementById("plot");
  await Plotly.newPlot(plot, data, layout);
  let i = 1;
  const updatePlot = async () => {
    if (i < rawData.length) {
      //trace2['x'] = rawData[i].map(p=>pixDensity*normalizeY(p.position[1])),
      //trace2['y'] = rawData[i].map(p=>pixDensity*normalizeX(p.position[0])),
      //trace2['z'] = rawData[i].map(p=>normalizeZ(chosenFuntion(p.position))),
      //await Plotly.redraw(plot)

      await Plotly.animate("plot", {
        data: [
          {
            x: rawData[i].map((p) => pixDensity * normalizeY(p.position[1])),
            y: rawData[i].map((p) => pixDensity * normalizeX(p.position[0])),
            z: rawData[i].map((p) =>
              normalizeZ(chosenFuntion(p.position) + ballShift)
            ),
          },
        ],
        traces: [1],
      });
      i += 1;
      window.requestAnimationFrame(updatePlot);
    } else {
    }
  };
  window.requestAnimationFrame(updatePlot);
};
await drawPlot();
