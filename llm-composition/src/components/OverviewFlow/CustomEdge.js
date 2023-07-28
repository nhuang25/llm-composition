import React from 'react';
import { getBezierPath, getMarkerEnd, EdgeText } from 'react-flow-renderer';

const CustomEdge = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  data,
  arrowHeadType,
  markerEndId,
}) => {
  const edgePath = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });
  const markerEnd = getMarkerEnd(arrowHeadType, markerEndId);
  const height = "200";
  const width = "500";


  return (
    <>
      <path id={id} style={style} className="react-flow__edge-path" d={edgePath} markerEnd={markerEnd} />
      <EdgeText
        x={(sourceX + (targetX - sourceX) / 2) - (width/2)}
        y={(sourceY + (targetY - sourceY) / 2)}
        label={"."}
        labelStyle={style}
        labelShowBg={false}
        labelTextAnchor="middle"
      >
        <foreignObject width={width} height={height}>
          <div xmlns="http://www.w3.org/1999/xhtml" style={{ width: '100%', wordWrap: 'break-word' }}>
            {data.label}
          </div>
        </foreignObject>
      </EdgeText>
    </>
  );
};

export default CustomEdge;