class Datum{
  position:[number, number]
  velocity:[number, number]
  constructor(){
    this.position = [1, 1]
    this.velocity = [1, 1]
  }
}
type Data = [[Datum]]
class Plotter{
  update = async ()=>true
  constructor(){
    this.update = async ()=>true
  }
}

const getMinPositionX = (data:Data) => Math.min(
  ...data.flatMap((x) => x.map((y) => y.position[0]))
);
const getMinPositionY = (data:Data)=> Math.min(
  ...data.flatMap((x) => x.map((y) => y.position[1]))
);
const getMaxPositionX = (data:Data) => Math.max(
  ...data.flatMap((x) => x.map((y) => y.position[0]))
);
const getMaxPositionY = (data:Data) => Math.max(
  ...data.flatMap((x) => x.map((y) => y.position[1]))
);

const rastrigin = (x:[number, number]) =>
  x.reduce(
    (acc, val) => acc + Math.pow(val, 2) - 10 * Math.cos(2 * Math.PI * val),
    0
  ) + 20;
const rosenbrock = (x:[number, number]) => {
  const a = 0;
  const b = 1;
  return Math.pow(a - x[0], 2) + b * Math.pow(x[1] - Math.pow(x[0], 2), 2);
};

const objectiveFunctions : Record<string, (c:[a:number, b:number])=>number> = {
  rosenbrock, rastrigin
}
const getPlotter = async (
    fileNames:string[],
    divName:string,
    objectiveFunctionName:string,
    type='contour'
    //objectiveFunction:(c:[a:number, b:number])=>number
): Promise<Plotter> => {
  const objectiveFunction = objectiveFunctions[objectiveFunctionName]
  const allData:Data[] = []
  for (const fileName of fileNames){
    const content = await (await fetch(fileName)).json() as unknown as Data
    allData.push(content)
  }
  const data = allData[0]
  const maxPositionX = getMaxPositionX(data)
  const maxPositionY = getMaxPositionY(data)
  const minPositionX = getMinPositionX(data)
  const minPositionY = getMinPositionY(data)
  const z_data = [];
  const pixDensity = 150;
  const xStep = (maxPositionX - minPositionX) / pixDensity;
  const yStep = (maxPositionY - minPositionY) / pixDensity;
  for (let i = 0; i < pixDensity; i++) {
    const row = [];
    for (let j = 0; j < pixDensity; j++) {
      const x = minPositionX + xStep * i;
      const y = minPositionY + yStep * j;
      row.push(objectiveFunction([x, y]));
    }
    z_data.push(row);
  }
  const min = Math.min(...z_data.flatMap((r) => r));
  const max = Math.max(...z_data.flatMap((r) => r));
  const normalizeZ = (y:number) => (y - min) / (max - min);
  const ballShift = (max - min) / 45;
  const normalizeX = (x:number) => (x - minPositionX) / (maxPositionX - minPositionX);
  const normalizeY = (x:number) => (x - minPositionY) / (maxPositionY - minPositionY);

  const fixedZData = z_data.map((x) => x.map(normalizeZ));
  const contourTrace = {
    z: fixedZData,
    type: type === "contour" ? 'contour' : 'surface',
  };
  const dataToTrace = (dati:Datum[], type='contour') => {
    const result = {
      x: dati.map((p) => pixDensity * normalizeY(p.position[1])),
      y: dati.map((p) => pixDensity * normalizeX(p.position[0])),
      type: type === 'contour' ? "scatter2d" : 'scatter3d',
      mode: "markers",
      marker: {
        size: type === 'contour' ? 10 : 5,
        line: {
          color: "rgba(217, 217, 217, 0.14)",
          width: 0.5,
        },
        opacity: 0.8,
      }
    }
    if (type === 'surface'){
      result['z'] = dati.map((p) => normalizeZ(objectiveFunction(p.position)) + 0.07)
    }
    return result
  };
  const normalize = (xs:number[])=>{
    const max = Math.max(...xs)
    const min = Math.min(...xs)
    return [max, min]
  }
  const contourParticleTrace = dataToTrace(data[0], type)
  if (type === 'surface'){
    //debugger;
  }
  const traces = [contourTrace, contourParticleTrace]
  if (fileNames.length > 1){
    traces.push(dataToTrace(allData[1][0]))
  }
  const contourPlot = document.getElementById(divName);
  await Plotly.newPlot(contourPlot, traces, {
    title: objectiveFunctionName,
    width: window.innerWidth / 2.1,
    height: window.innerHeight,
    scene: {
      camera: {
        eye:
          objectiveFunctionName === "rastrigin"
            ? { x: 0.8, y: -0.8, z: 1.5 }
            : {},
      },
    },
  });
  const getValues = (i:number, dati:Datum[]) => dati.map(
          (p) => pixDensity * normalizeY(p.position[i])
        );

  let i = 0
  const plotter = {
    'update':async ()=>{
      if (i < data.length) {
        //contourParticleTrace.x = [pixDensity * normalizeY(rawDataGD[i][1])]
        //contourParticleTrace.y = [pixDensity * normalizeX(rawDataGD[i][0])]
        //
        contourParticleTrace.x = getValues(1, data[i])
        contourParticleTrace.y = getValues(0 , data[i])
        if (type === 'surface'){
          contourParticleTrace['z'] = data[i].map((p) => normalizeZ(objectiveFunction(p.position)) + 0.07)
        }
        if (allData.length > 1){
          traces.at(-1)!.x = getValues(0, allData.at(1)[i])
          traces.at(-1)!.y = getValues(1, allData.at(1)[i])
          if (type === 'surface'){
            traces.at(-1)['z'] = allData.at(1)[i].map((p) => normalizeZ(objectiveFunction(p.position)) + 0.07)
          }
        }
        await Plotly.redraw(contourPlot);
        i += 1
      return false
    }
    return true
  }
  }
  return plotter as unknown as Plotter
}

export {Datum, getPlotter}
