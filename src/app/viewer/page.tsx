'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { Play, Pause, SkipBack, SkipForward, Download, Home, Volume2, VolumeX } from 'lucide-react';

export default function ViewerPage() {
  const router = useRouter();
  const [projects, setProjects] = useState<any[]>([]);
  const [selectedProject, setSelectedProject] = useState<any>(null);
  const [scenes, setScenes] = useState<any[]>([]);
  const [currentSceneIndex, setCurrentSceneIndex] = useState(0);
  const [currentFrameData, setCurrentFrameData] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [frameIndex, setFrameIndex] = useState(0);
  const [totalFrames, setTotalFrames] = useState(0);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const result = await api.listProjects();
      setProjects(result);
      if (result.length > 0) {
        setSelectedProject(result[0]);
        loadScenes(result[0].id);
      }
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
    setLoading(false);
  };

  const loadScenes = async (projectId: string) => {
    try {
      const project = await api.getProject(projectId);
      setScenes(project.scenes || []);
      setCurrentSceneIndex(0);
      setFrameIndex(0);
      if (project.scenes && project.scenes.length > 0) {
        loadScenePreview(project.scenes[0].id);
      }
    } catch (error) {
      console.error('Failed to load scenes:', error);
    }
  };

  const loadScenePreview = async (sceneId: string) => {
    try {
      const svg = await api.previewScene(sceneId);
      setCurrentFrameData(svg);
      setTotalFrames(Math.ceil((scenes[currentSceneIndex]?.duration || 3) * 30)); // 30 FPS
    } catch (error) {
      console.error('Failed to load scene preview:', error);
    }
  };

  useEffect(() => {
    if (!isPlaying || scenes.length === 0) return;

    const interval = setInterval(() => {
      setFrameIndex((prev) => {
        const nextFrame = prev + 1;
        if (nextFrame >= totalFrames) {
          if (currentSceneIndex < scenes.length - 1) {
            setCurrentSceneIndex(currentSceneIndex + 1);
            loadScenePreview(scenes[currentSceneIndex + 1].id);
            return 0;
          } else {
            setIsPlaying(false);
            return prev;
          }
        }
        return nextFrame;
      });
    }, 1000 / 30); // 30 FPS

    return () => clearInterval(interval);
  }, [isPlaying, currentSceneIndex, scenes, totalFrames]);

  const handleProjectSelect = (project: any) => {
    setSelectedProject(project);
    loadScenes(project.id);
  };

  const handlePreviousScene = () => {
    if (currentSceneIndex > 0) {
      setCurrentSceneIndex(currentSceneIndex - 1);
      setFrameIndex(0);
      loadScenePreview(scenes[currentSceneIndex - 1].id);
    }
  };

  const handleNextScene = () => {
    if (currentSceneIndex < scenes.length - 1) {
      setCurrentSceneIndex(currentSceneIndex + 1);
      setFrameIndex(0);
      loadScenePreview(scenes[currentSceneIndex + 1].id);
    }
  };

  const handleExport = async () => {
    if (!selectedProject) return;
    try {
      alert('Export started. This may take a few minutes...');
      const result = await api.exportVideo(selectedProject.id);
      alert('Export completed! Video saved to storage/videos/');
    } catch (error) {
      alert('Export failed: ' + (error as any).message);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center min-h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-black border-b border-gray-700 p-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <button
            onClick={() => router.push('/projects')}
            className="bg-gray-800 hover:bg-gray-700 p-2 rounded transition"
            title="Back to projects"
          >
            <Home size={20} />
          </button>
          <h1 className="text-2xl font-bold">Animation Viewer</h1>
        </div>
        <button
          onClick={handleExport}
          disabled={!selectedProject}
          className="bg-green-600 hover:bg-green-700 disabled:opacity-50 px-4 py-2 rounded flex items-center gap-2 transition"
        >
          <Download size={16} /> Export MP4
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4 h-screen">
        {/* Project List */}
        <div className="bg-gray-800 border-r border-gray-700 overflow-y-auto">
          <div className="p-4 border-b border-gray-700">
            <h2 className="font-bold mb-2">Projects</h2>
          </div>
          <div className="space-y-2 p-4">
            {projects.map((project) => (
              <button
                key={project.id}
                onClick={() => handleProjectSelect(project)}
                className={`w-full text-left p-3 rounded transition ${
                  selectedProject?.id === project.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 hover:bg-gray-600 text-gray-100'
                }`}
              >
                <div className="font-semibold truncate">{project.name}</div>
                <div className="text-xs text-gray-300">{project.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Main Viewer */}
        <div className="col-span-2 flex flex-col">
          {/* Canvas */}
          <div className="flex-1 bg-black flex items-center justify-center p-4 overflow-auto">
            {currentFrameData ? (
              <div className="w-full h-full flex items-center justify-center">
                <div
                  dangerouslySetInnerHTML={{ __html: currentFrameData }}
                  className="max-w-full max-h-full"
                />
              </div>
            ) : (
              <div className="text-gray-500 text-center">
                <div className="mb-2">No scenes to display</div>
                <div className="text-sm">Create a story first or select a project with scenes</div>
              </div>
            )}
          </div>

          {/* Playback Controls */}
          <div className="bg-gray-800 border-t border-gray-700 p-4 space-y-4">
            {/* Frame Info */}
            <div className="text-sm text-gray-400">
              <div className="flex justify-between mb-2">
                <span>Scene {currentSceneIndex + 1} of {scenes.length}</span>
                <span>Frame {frameIndex + 1} of {totalFrames}</span>
              </div>
              <div className="text-xs text-gray-500">
                {scenes[currentSceneIndex]?.title || 'Scene ' + (currentSceneIndex + 1)}
              </div>
            </div>

            {/* Timeline */}
            <input
              type="range"
              min="0"
              max={totalFrames - 1}
              value={frameIndex}
              onChange={(e) => setFrameIndex(parseInt(e.target.value))}
              className="w-full cursor-pointer"
            />

            {/* Controls */}
            <div className="flex gap-2 justify-center items-center flex-wrap">
              <button
                onClick={handlePreviousScene}
                disabled={currentSceneIndex === 0}
                className="bg-gray-700 hover:bg-gray-600 disabled:opacity-50 p-2 rounded transition"
                title="Previous scene"
              >
                <SkipBack size={16} />
              </button>

              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded flex items-center gap-2 transition"
              >
                {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                {isPlaying ? 'Pause' : 'Play'}
              </button>

              <button
                onClick={handleNextScene}
                disabled={currentSceneIndex === scenes.length - 1}
                className="bg-gray-700 hover:bg-gray-600 disabled:opacity-50 p-2 rounded transition"
                title="Next scene"
              >
                <SkipForward size={16} />
              </button>

              <button
                onClick={() => setIsMuted(!isMuted)}
                className="bg-gray-700 hover:bg-gray-600 p-2 rounded transition ml-auto"
                title={isMuted ? 'Unmute audio' : 'Mute audio'}
              >
                {isMuted ? <VolumeX size={16} /> : <Volume2 size={16} />}
              </button>
            </div>

            {/* Narration */}
            {scenes[currentSceneIndex]?.narration && (
              <div className="bg-gray-700 p-3 rounded text-sm">
                <div className="font-semibold mb-1 text-gray-300">Narration:</div>
                <div className="text-gray-200">{scenes[currentSceneIndex].narration}</div>
              </div>
            )}
          </div>
        </div>

        {/* Scene List */}
        <div className="bg-gray-800 border-l border-gray-700 overflow-y-auto">
          <div className="p-4 border-b border-gray-700">
            <h2 className="font-bold mb-2">Scenes</h2>
            <div className="text-xs text-gray-400">{scenes.length} scenes</div>
          </div>
          <div className="space-y-2 p-4">
            {scenes.map((scene, idx) => (
              <button
                key={scene.id}
                onClick={() => {
                  setCurrentSceneIndex(idx);
                  setFrameIndex(0);
                  loadScenePreview(scene.id);
                }}
                className={`w-full text-left p-3 rounded transition border-l-4 ${
                  currentSceneIndex === idx
                    ? 'bg-blue-900 border-blue-500 text-white'
                    : 'bg-gray-700 border-gray-600 hover:bg-gray-600 text-gray-100'
                }`}
              >
                <div className="font-semibold text-sm">Scene {idx + 1}</div>
                <div className="text-xs text-gray-300 mt-1">{scene.title || 'Untitled'}</div>
                <div className="text-xs text-gray-400 mt-1">
                  Background: {scene.background}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Duration: {scene.duration}s
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
