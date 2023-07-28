import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';

export default memo(({ data, isConnectable }) => {
  return (
    <>
      <Handle
        type="target"
        position={Position.Top}
        id="b"
        style={{ left: 10, background: '#555' }}
        onConnect={(params) => console.log('handle onConnect', params)}
        isConnectable={isConnectable}
      />
      <div>
        data.label
      </div>
      <Handle
        type="source"
        position={Position.Top}
        id="a"
        style={{ right: 10, background: '#555' }}
        isConnectable={isConnectable}
      />
    </>
  );
});
