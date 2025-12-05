'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Play, Pause, Download } from 'lucide-react';

export default function AnimationViewer({ projectId }: { projectId: string }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [frames, setFrames] = useState<any[]>([]);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadFrames();
  }, [projectId]);

  const loadFrames = async () => {
    setLoading(true);
    try {
      const result = await api.renderAnimation(projectId);
      // In a real implementation, we'd load actual frame data
      setFrames(new Array(30).fill(null)); // Placeholder
    } catch (error) {
      console.error('Failed to load frames:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      setCurrentFrame((prev) => (prev + 1) % frames.length);
    }, 1000 / 30); // 30 FPS

    return () => clearInterval(interval);
  }, [isPlaying, frames.length]);

  if (loading) {
    return <div className="text-center py-8">Rendering animation...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="bg-black rounded-lg aspect-video flex items-center justify-center min-h-96">
        <div className="text-gray-500">
          {frames.length > 0 ? `Frame ${currentFrame + 1}/${frames.length}` : 'No frames'}
        </div>
      </div>

      <div className="flex gap-4 items-center">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center gap-2"
        >
          {isPlaying ? <Pause size={16} /> : <Play size={16} />}
          {isPlaying ? 'Pause' : 'Play'}
        </button>

        <input
          type="range"
          min="0"
          max={Math.max(0, frames.length - 1)}
          value={currentFrame}
          onChange={(e) => setCurrentFrame(parseInt(e.target.value))}
          className="flex-1"
        />

        <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 flex items-center gap-2">
          <Download size={16} /> Export MP4
        </button>
      </div>
    </div>
  );
}
