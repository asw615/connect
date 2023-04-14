d3.csv("data/survey.csv").then(data => {
  const width = 1000;
  const height = 1000;

  const uniqueClasses = Array.from(new Set(data.map(d => d.class)));

  // Create the dropdown menu
  const select = d3.select("body").append("select")
    .on("change", updateGraph);

  // Add "All" option
  select.append("option")
    .text("All")
    .attr("value", "all");

  // Add class options
  select.selectAll("option.class")
    .data(uniqueClasses)
    .enter()
    .append("option")
    .attr("class", "class")
    .text(d => d)
    .attr("value", d => d);

  const svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

  // Tooltip
  const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

  // Main graph function
  function updateGraph() {
    const selectedClass = select.property("value");
    const filteredData = selectedClass === "all" ? data : data.filter(d => d.class === selectedClass);

    const nodes = filteredData.map(d => ({ id: d.name }));
    const links = updateLinks(filteredData);
    const linkColors = updateLinkColors(filteredData);

    updateNodes(nodes, links, linkColors);
  }

  function updateLinks(filteredData) {
    const links = [];
    filteredData.forEach(row => {
      const name = row.name;

      row.work_well.split(',').forEach(work_well => {
        work_well = work_well.trim();
        if (work_well) {
          const linkKey = `${name}-${work_well}`;
          const reversedLinkKey = `${work_well}-${name}`;
          if (!links.some(link => (link.source === name && link.target === work_well) || (link.source === work_well && link.target === name))) {
            links.push({source: name, target: work_well, key: linkKey, reversedKey: reversedLinkKey});
          }
        }
      });

      row.not_work_well.split(',').forEach(not_work_well => {
        not_work_well = not_work_well.trim();
        if (not_work_well) {
          const linkKey = `${name}-${not_work_well}`;
          const reversedLinkKey = `${not_work_well}-${name}`;
          if (!links.some(link => (link.source === name && link.target === not_work_well) || (link.source === not_work_well && link.target === name))) {
            links.push({source: name, target: not_work_well, key: linkKey, reversedKey: reversedLinkKey});
          }
        }
      });
    });
    return links;
  }

  function updateLinkColors(filteredData) {
    const linkColors = {};
    updateLinks(filteredData).forEach(link => {
      if (!linkColors.hasOwnProperty(link.key) && !linkColors.hasOwnProperty(link.reversedKey)) {
        linkColors[link.key] = 'blue';
        } else if (!linkColors.hasOwnProperty(link.key) && !linkColors.hasOwnProperty(link.reversedKey)) {
          linkColors[link.key] = 'orange';
        } else if (linkColors.hasOwnProperty(link.reversedKey) && linkColors[link.reversedKey] === 'orange') {
          linkColors[link.reversedKey] = 'red';
        }
      });
      return linkColors;
    }
  
    function updateNodes(nodes, links, linkColors) {
      svg.selectAll(".links, .nodes, .labels").remove();
  
      const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(300))
        .force("charge", d3.forceManyBody().strength(-800))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .alphaDecay(0.5);
  
      const link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter().append("line")
        .style("stroke", d => linkColors[d.key]);
  
      const node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter().append("circle")
        .attr("r", 20)
        .style("fill", "lightblue")
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended))
        .on("mouseover", showTooltip)
        .on("mousemove", moveTooltip)
        .on("mouseout", hideTooltip);
  
      // Add labels to nodes
      const labels = svg.append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(nodes)
        .enter().append("text")
        .attr("dy", ".35em")
        .style("font-size", "15px")
        .style("fill", "black")
        .text(d => d.id);
  
      simulation
        .nodes(nodes)
        .on("tick", ticked);
  
      simulation.force("link")
        .links(links);
  
      function ticked() {
        link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
  
        node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
  
        labels
          .attr("x", d => d.x)
          .attr("y", d => d.y);
      }
    }
  
    // Tooltip functions
      function showTooltip(d) {
    const person = data.find(person => person.name === d.id);
    const worksWellWith = person.work_well.split(',').map(s => s.trim()).filter(Boolean).join(', ');
    const notWorksWellWith = person.not_work_well.split(',').map(s => s.trim()).filter(Boolean).join(', ');

    tooltip.transition()
      .duration(500)
      .style("opacity", 0.9);

    tooltip.html(`<strong>${d.id}</strong><br><br><u>Works well with:</u><br>${worksWellWith || 'N/A'}<br><br><u>Doesn't work well with:</u><br>${notWorksWellWith || 'N/A'}`)
      .style("left", "20px")
      .style("bottom", "20px");
  }

  function moveTooltip(d) {
    tooltip
      .style("left", (d3.event.pageX + 20) + "px")
      .style("top", (d3.event.pageY - 20) + "px");
  }

  function hideTooltip(d) {
    tooltip.transition()
      .duration(500)
      .style("opacity", 0);
  }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  updateGraph();
});
