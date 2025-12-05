'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import CharacterSelector from './CharacterSelector';
import AudioGenerator from './AudioGenerator';
import { Camera, Trash2 } from 'lucide-react';

export default function SceneEditor({ scene, projectId, onSceneDeleted }: { scene: any; projectId: string; onSceneDeleted?: () => void }) {
  const [sceneData, setSceneData] = useState(scene);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setSceneData(scene);
    loadPreview();
  }, [scene]);

  const loadPreview = async () => {
    try {
      const svg = await api.previewScene(scene.id);
      setPreview(svg);
    } catch (error) {
      console.error('Failed to load preview:', error);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      await api.updateScene(scene.id, sceneData);
      await loadPreview();
      alert('Scene saved!');
    } catch (error) {
      alert('Failed to save scene');
    }
    setLoading(false);
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this scene?')) {
      return;
    }

    setLoading(true);
    try {
      await api.deleteScene(scene.id);
      alert('Scene deleted!');
      if (onSceneDeleted) {
        onSceneDeleted();
      }
    } catch (error) {
      alert('Failed to delete scene');
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h3 className="font-bold mb-4 flex items-center gap-2">
            <Camera size={20} /> Preview
          </h3>
          {preview && (
            <div className="bg-gray-200 rounded-lg p-2">
              <div
                dangerouslySetInnerHTML={{ __html: preview }}
                className="w-full border rounded"
              />
            </div>
          )}
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Scene Narration 
              <span className="text-xs text-blue-600 ml-2">(Auto-generated - Edit if needed)</span>
            </label>
            <textarea
              value={sceneData.narration || ''}
              onChange={(e) => setSceneData({ ...sceneData, narration: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Duration (seconds)</label>
            <input
              type="number"
              value={sceneData.duration || 3}
              onChange={(e) => setSceneData({ ...sceneData, duration: parseFloat(e.target.value) })}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="1"
              step="0.5"
            />
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleSave}
              disabled={loading}
              className="flex-1 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
            <button
              onClick={handleDelete}
              disabled={loading}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 flex items-center gap-2"
              title="Delete this scene"
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>
      </div>

      <div className="border-t pt-6">
        <h3 className="font-bold mb-4">Characters</h3>
        <CharacterSelector scene={sceneData} onUpdate={setSceneData} />
      </div>

      <div className="border-t pt-6">
        <h3 className="font-bold mb-4">Audio</h3>
        <AudioGenerator projectId={projectId} sceneId={scene.id} text={sceneData.narration} />
      </div>
    </div>
  );
}
