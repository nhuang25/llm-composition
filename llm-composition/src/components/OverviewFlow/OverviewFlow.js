import React, { useCallback, useEffect, useState } from 'react';
import ReactFlow, {
  addEdge,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from 'reactflow';
// import useWebSocket from 'react-use-websocket';
import { io } from 'socket.io-client';
import InitialAsk from './InitialAsk';
import Dialog from './Dialog';

import { nodes as initialNodes, edges as initialEdges } from './initial-elements';
import CustomNode from './CustomNode';
import CustomEdge from './CustomEdge';

import 'reactflow/dist/style.css';
import './overview.css';

const nodeTypes = {
  custom: CustomNode,
};

const minimapStyle = {
  height: 120,
};

const id_to_name_mapping = {
  '1': 'Dispatcher',
  '2': 'Plant Health Bot',
  '3': 'Production Output Bot',
  '4': 'Distribution Bot',
  '5': 'Human Resources Bot'
}
const id_to_color_mapping = {
  '1': '#ef476f',
  '2': '#ec9706',
  '3': '#06d6a0',
  '4': '#118ab2',
  '5': '#073b4c'
}

const onInit = (reactFlowInstance) => console.log('flow loaded:', reactFlowInstance);

const OverviewFlow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [initialAsk, setInitialAsk] = useState("");
  const [messages, setMessages] = useState([]);
  const [finished, setFinished] = useState(false);
  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), []);

  /* Sockets Approach */
  useEffect(() => {
    const socket = io('http://localhost:5000');

    socket.on('addEdge', (data) => {
      if (data.type === 'addEdge') {
        setMessages((prevMessages) => [...prevMessages, data.edge]);
        setEdges([])
        setEdges((eds) => addEdge(data.edge, eds));
      }
    });

    socket.on('action', (data) => {
      if (data.type === 'action') {
        setMessages((prevMessages) => [...prevMessages, data.action]);
      }
    });

    socket.on('initialAsk', (data) => {
      if (data.type === 'initialAsk') {
        setFinished(false)
        setInitialAsk(data.ask)
        setMessages([])
        setEdges([])
      }
    });

    socket.on('askFinished', (data) => {
      if (data.type === 'askFinished') {
        setEdges([])
        setFinished(true)
      }
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const edgeTypes = {
    "customEdge": CustomEdge,
  };

  return (
    <div class="row" style={{ width: '100vw', height: '100vh' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          edgeTypes={edgeTypes}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onInit={onInit}
          fitView
          attributionPosition="top-right"
          nodeTypes={nodeTypes}
          style={{ width: '50%', height: '100%' }}
        >
          <MiniMap style={minimapStyle} zoomable pannable />
          <Controls />
          <Background color="#aaa" gap={16} />
        </ReactFlow>
        <div class='column' style={{ width: '50%', overflowY: 'auto'}}>
          <InitialAsk ask={initialAsk}/>
          {messages.map((item, index) => (
            <Dialog
              source_name={id_to_name_mapping[item.source]}
              source_color={id_to_color_mapping[item.source]}
              target_name={id_to_name_mapping[item.target]}
              target_color={id_to_color_mapping[item.target]}
              message={item.data.label}
            />
          ))}
          {
            finished && <div class="finishedBox">
               Finished Successfully!
            </div>
          }    
        </div>
    </div>
  );
};

export default OverviewFlow;
