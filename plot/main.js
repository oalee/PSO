const drawPlot = async () => {
  const rawData = await (await fetch("positions.json")).json();
  const minPositionX = Math.min(
    ...rawData.flatMap((x) => x.map((y) => y.position[0]))
  );
  const minPositionY = Math.min(
    ...rawData.flatMap((x) => x.map((y) => y.position[0]))
  );
  const maxPositionX = Math.max(
    ...rawData.flatMap((x) => x.map((y) => y.position[0]))
  );
  const maxPositionY = Math.max(
    ...rawData.flatMap((x) => x.map((y) => y.position[0]))
  );

  /*
  def f_rosenbrock(x):
 13     a = 0
 14     b = 1
 15     return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2
 */
  const rosenbrock = (x) => {
    const a = 0;
    const b = 1;
    return Math.pow(a - x[0], 2) + b * Math.pow(x[1] - Math.pow(x[0], 2), 2);
  };

  var z_data = [];
  let x = minPositionX;
  const pixDensity = 100;
  const xStep = (maxPositionX - minPositionX) / pixDensity;
  const yStep = (maxPositionY - minPositionY) / pixDensity;
  for (let i = 0; i < pixDensity; i++) {
    for (let j = 0; j < pixDensity; j++) {
      z_data.push(rosenbrock([xStep * i, yStep * j]));
    }
  }

  const data = [
    {
      z: z_data,
      type: "surface",
    },
  ];

  var layout = {
    title: "Mt Bruno Elevation",
    autosize: false,
    width: 1000,
    height: 1000,
    margin: {
      l: 65,
      r: 50,
      b: 65,
      t: 90,
    },
  };
  Plotly.newPlot("plot", data, layout);
};

await drawPlot();
