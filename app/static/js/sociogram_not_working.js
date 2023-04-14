// Read the CSV file and generate the sociogram visualization
d3.csv('data/Sociogram survey(1-10).csv').then(function(data) {
  // Convert the data to nodes and links
  const nodes = data.map(d => ({ name: d.name }));
  const links = data.flatMap(function(d) {
    return [
      { source: d.name, target: d.work_well, value: 1 },
      { source: d.name, target: d.not_work_well, value: -1 }
    ];
  });

  // Define the dimensions of the visualization
  const width = 600;
  const height = 400;

  // Create the SVG container
  const svg = d3.select('#sociogram')
    .attr('width', width)
    .attr('height', height);

  // Define the simulation
  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.index))
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(width / 2, height / 2));

  // Add the links
  const link = svg.append('g')
    .attr('stroke', '#999')
    .attr('stroke-opacity', 0.6)
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('stroke-width', d => Math.abs(d.value) * 2);

  // Add the nodes
  const node = svg.append('g')
    .attr('stroke', '#fff')
    .attr('stroke-width', 1.5)
    .selectAll('circle')
    .data(nodes)
    .join('circle')
    .attr('r', 10)
    .attr('fill', 'blue')
    .call(drag(simulation));

  // Add the node labels
  const label = svg.append('g')
    .attr('class', 'labels')
    .selectAll('text')
    .data(nodes)
    .join('text')
    .attr('dx', 15)
    .attr('dy', 5)
    .text(d => d.name);

  // Add the tick function to update the positions of the nodes and links
  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y);

    label
      .attr('x', d => d.x)
      .attr('y', d => d.y);
  });
