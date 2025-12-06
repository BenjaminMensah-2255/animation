'use client';

import { useState, useEffect, use } from 'react';
import { api } from '@/lib/api';
import StoryCreator from '@/components/StoryCreator';
import SceneEditor from '@/components/SceneEditor';
import { Play, Save } from 'lucide-react';

export default function Editor({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const projectId = id;
  const [project, setProject] = useState<any>(null);
  const [activeScene, setActiveScene] = useState<any>(null);
  const [tab, setTab] = useState<'story' | 'scenes' | 'edit'>('story');
  const [loading, setLoading] = useState(true);
  const [generatedStory, setGeneratedStory] = useState<any>(null);

  useEffect(() => {
    loadProject();
  }, [projectId]);

  const loadProject = async () => {
    try {
      const result = await api.getProject(projectId);
      setProject(result);
      if (result.scenes && result.scenes.length > 0) {
        setActiveScene(result.scenes[0]);
      }
    } catch (error) {
      console.error('Failed to load project:', error);
    }
    setLoading(false);
  };

  if (loading || !project) {
    return <div className="flex justify-center items-center min-h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white shadow-sm p-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">{project.name}</h1>
          <div className="flex gap-2">
            <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center gap-2">
              <Play size={16} /> Preview
            </button>
            <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 flex items-center gap-2">
              <Save size={16} /> Save
            </button>
          </div>
        </div>

        <div className="flex gap-4 p-4">
          <div className="flex-1">
            <div className="bg-white rounded-lg shadow p-4">
              <div className="flex gap-2 border-b mb-4">
                <button
                  onClick={() => setTab('story')}
                  className={`px-4 py-2 ${tab === 'story' ? 'border-b-2 border-blue-600 text-blue-600' : ''}`}
                >
                  Story
                </button>
                <button
                  onClick={() => setTab('scenes')}
                  className={`px-4 py-2 ${tab === 'scenes' ? 'border-b-2 border-blue-600 text-blue-600' : ''}`}
                >
                  Scenes
                </button>
                <button
                  onClick={() => setTab('edit')}
                  className={`px-4 py-2 ${tab === 'edit' ? 'border-b-2 border-blue-600 text-blue-600' : ''}`}
                >
                  Edit
                </button>
              </div>

              {tab === 'story' && <StoryCreator projectId={projectId} onStoryCreated={loadProject} generatedStory={generatedStory} onStoryGenerated={setGeneratedStory} />}
              {tab === 'scenes' && (
                <div className="space-y-4">
                  {project.scenes && project.scenes.length > 0 ? (
                    project.scenes.map((scene: any) => (
                      <div
                        key={scene.id}
                        onClick={() => {
                          setActiveScene(scene);
                          setTab('edit');
                        }}
                        className="p-4 border rounded hover:bg-gray-50 cursor-pointer transition"
                      >
                        <h3 className="font-bold">Scene {scene.sequence}: {scene.title || 'Untitled'}</h3>
                        <p className="text-sm text-gray-600 mt-2"><strong>Background:</strong> {scene.background}</p>
                        <p className="text-sm text-gray-700 mt-2"><strong>Narration:</strong> {scene.narration?.substring(0, 100)}...</p>
                        <div className="text-xs text-blue-600 mt-2">📻 Audio ready - Click to edit</div>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500">No scenes yet. Create a story first in the Story tab.</p>
                  )}
                </div>
              )}
              {tab === 'edit' && activeScene && <SceneEditor scene={activeScene} projectId={projectId} onSceneDeleted={() => { loadProject(); setTab('scenes'); }} />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
