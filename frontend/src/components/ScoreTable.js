import { TreeTable } from 'primereact/treetable';
import { Column } from 'primereact/column';

export function ScoreTable(props){
    const { data } = props
    return (
        <TreeTable value={getNodes(data, Object.keys(data))} scrollable scrollHeight="400px">
            <Column field="name" header="Name" expander></Column>
            <Column field="question" header="Question"></Column>
            <Column field="score" header="Score"></Column>
        </TreeTable>
    )
}

const getNodes = (data, methods) => {
    let nodes = []
    console.log(methods)
    console.log(data)
    methods.forEach((method, index) => {
        const node = {}
        node['key'] = index;
        node['label'] = method
        node['data'] = {
            "name": method
        }
        node.children = data[method].map((children, childIndex) => ({
            key: `${index}-${childIndex}`,
            data: {
                "question": children.question,
                "score": children.score || children.score[0]
            }
        }))

        nodes = [...nodes, node]
    })

    return nodes
}
