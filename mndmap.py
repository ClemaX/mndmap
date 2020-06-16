import sys
import pydot

class MndParser:
	@staticmethod
	def parse(filename):
		try:
			file = open(filename, 'r')
		except FileNotFoundError as e:
			return (None)
		else:
			parsed = {}
			path = []
			with file:
				for line in file:
					indent = 0
					while line[indent] == '\t': indent += 1
					if line[indent] == '-':
						label = line[indent + 1:].strip()
						value = parsed
						
						for k in path[:indent]:
							value = value[k]
						value[label] = {}

						if indent == len(path):
							path.append(label)
						elif indent < len(path):
							path[indent] = label
						elif indent != 0:
							raise NotImplementedError("Indentation must be linear")
					elif line[indent] != '\n':
						raise NotImplementedError(f"'{line[indent]}' not supported")
			return parsed

class MndRenderer:
	def __draw(self, parent, child):
		edge = pydot.Edge(parent, child)
		self.graph.add_edge(edge)

	def __visit(self, node, parent=None):
		for k, v in node.items():
			if isinstance(v, dict):
				if parent:
					self.__draw(parent, k)
				self.__visit(v, k)
			else:
				self.__draw(parent, k)
				self.__draw(k, v)

	def __init__(self, data):
		self.graph = pydot.Dot(graph_type='digraph')
		self.__visit(data)

	def write_png(self, out_file='out.png'):
		self.graph.write_png(out_file)

if __name__ == '__main__':
	ac = len(sys.argv)
	if ac == 1 or ac > 3:
		exit(1)
	in_file = sys.argv[1]
	out_file = sys.argv[2] if ac == 3 else 'out.png'
	data = MndParser.parse(in_file)
	renderer = MndRenderer(data)
	renderer.write_png(out_file)
