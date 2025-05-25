// src/components/ReplayViewer.jsx
import React, { useEffect, useRef } from 'react';
import { WebViewer } from '@rerun-io/web-viewer';

const ReplayViewer = ({ rrdUrl }) => {
    const containerRef = useRef(null);

    useEffect(() => {
        if (!rrdUrl) return;

        const viewer = new WebViewer();
        viewer.start(rrdUrl, containerRef.current, {
            width: '100%',
            height: '100%',
        });

        return () => {
            viewer.stop();
        };
    }, [rrdUrl]);

    return (
        <div
            ref={containerRef}
            style={{ width: '100%', height: '600px' }}
        />
    );
};

export default ReplayViewer;
