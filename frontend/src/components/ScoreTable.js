import { TreeTable } from 'primereact/treetable';
import { Column } from 'primereact/column';

export function ScoreTable(props) {
  const { data } = props;
  return (
    <TreeTable
      value={getNodes(data, Object.keys(data))}
      scrollable
      scrollHeight="400px"
    >
      <Column field="name" header="Name" expander></Column>
      <Column field="question" header="Question"></Column>
      <Column field="answer" header="Answer"></Column>
      <Column field="score" header="Score"></Column>
    </TreeTable>
  );
}

const getNodes = (data, methods) => {
  let nodes = [];
  methods.forEach((method, index) => {
    const node = {};
    node['key'] = index;
    node['label'] = method;
    node['data'] = {
      name: method.charAt(0).toUpperCase() + method.slice(1),
    };
    node.children = data[method].map((children, childIndex) => ({
      key: `${index}-${childIndex}`,
      data: {
        question: children.question,
        answer: children.answer,
        score: Array.isArray(children.score)
          ? children.score[0]
          : children.score,
      },
    }));

    nodes = [...nodes, node];
  });

  return nodes;
};
