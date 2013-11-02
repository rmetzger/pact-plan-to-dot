#/usr/bin/python2.7


#
# Generate nice Graphviz Graph from Pact Plan
#
#	 dot -Tsvg plan.dot -o plan.svg
#
#
# Author: Robert Metzger (robertmetzger.de)
#

import json
import re
import ntpath

def beautifyName(name):
	if re.match( r'(file|hdfs):(.*)', name):
		return ntpath.basename(name)
	return name

# Palette taken from http://www.colourlovers.com/palette/580974/Adrift_in_Dreams (let the experts do that stuff)
colors = {
	"sourceData Source" 	: "#cff09e",
	"pactMap" 		: "#a8dba8",
	"pactReduce" 		: "#79bd9a",
	"pactMatch" 		: "#3b8686",
	"sinkData Sink"		: "#0b486b"
}
# used to create printable names for the legend
niceColorNames = {
	"sourceData Source" : "Data Source",
	"sinkData Sink" : "Data Sink",
}
shape = {
	"source"	: "doublecircle",
	"pact"		: "box",
	"sink"		: "folder"
}


out = open('plan.dot', 'w')

json_data = open("plan.json")

data = json.load(json_data)

out.write("digraph plan {\n\trankdir=\"LR\";\n")

sources = []
sinks = []
# write nodes
for node in data["nodes"]:
	if node["type"] == "source":
		sources.append(node["id"])
	if node["type"] == "sink":
		sinks.append(node["id"])
	# node attributes
	out.write("\t"+str(node["id"])+" [label=\""+beautifyName(node["contents"])+"\",shape=\""+shape[node["type"]]+"\",style=filled, fillcolor=\""+colors[node["type"]+node["pact"]]+"\"]\n")
	# write connections
	if "predecessors" in node:
		predecessors = node["predecessors"]
		for pre in predecessors:
			out.write( "\t"+str(pre["id"]) + " -> "+ str(node["id"])+";\n")

# write ranks (to order sources and sinks:{rank=same; 5  11 35  48};
out.write("{rank=same; ");
for source in sources:
	out.write(str(source)+" ");
out.write("}\n{rank=same; ");
for sink in sinks:
	out.write(str(sink)+" ");
out.write("}\n");
# Write label http://stackoverflow.com/questions/3499056/making-a-legend-key-in-graphviz
out.write("""{ rank = sink;
Legend [shape=none, margin=0, label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
<TR>
  <TD COLSPAN="2"><B>Legend</B></TD>
</TR>""");

for element,color in colors.items():
	el = niceColorNames.get(element,element)
	out.write(" <TR><TD>"+el+"</TD><TD BGCOLOR=\""+color+"\"></TD></TR>")

out.write("""</TABLE>
>];
}""");

out.write("}")


