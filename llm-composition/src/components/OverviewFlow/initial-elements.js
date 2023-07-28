import React from 'react';
import { MarkerType, Position } from 'reactflow';

export const nodes = [
  {
    id: '1',
    data: {
      label: 'Dispatcher',
    },
    style: {
      background: '#ef476f',
      color: "white",
      fontWeight: "bold"
    },
    position: { x: 400, y: -300 },
    sourcePosition: Position.Bottom,
    targetPosition: Position.Bottom
  },
  {
    id: '2',
    data: {
      label: 'Plant Health',
    },
    style: {
      background: '#ec9706',
      color: "white",
      fontWeight: "bold"
    },
    position: { x: -150, y: -50 },
    sourcePosition: Position.Right,
    targetPosition: Position.Top
  },
  {
    id: '3',
    data: {
      label: 'Production Output',
    },
    style: {
      background: '#06d6a0',
      color: "white",
      fontWeight: "bold"
    },
    position: { x: 150, y: 150 },
    sourcePosition: Position.Right,
    targetPosition: Position.Top
  },
  {
    id: '4',
    data: {
      label: 'Distribution',
    },
    style: {
      background: '#118ab2',
      color: "white",
      fontWeight: "bold"
    },
    position: { x: 650, y: 150 },
    sourcePosition: Position.Left,
    targetPosition: Position.Top
  },
  {
    id: '5',
    data: {
      label: 'Human Resources',
    },
    style: {
      background: '#073b4c',
      color: "white",
      fontWeight: "bold"
    },
    position: { x: 950, y: -50 },
    sourcePosition: Position.Left,
    targetPosition: Position.Top
  }
];

export const edges = [
//   {
//     "id": "ahhh",
//     "source": "1",
//     "target": "2",
//     "animated": "True",
//     "type": "customEdge",
//     "data": {"label": "Hello my name is Nick and I love star wars especially the Clone Wars. Adjust the Production Allocation Plan for Stuffed Animal Plant 8 to account for the downtime of the ocelot making machine during repair (WO013) from 2023-01-01 to 2023-01-03."}
// }
];
