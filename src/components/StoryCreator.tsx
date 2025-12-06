'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Wand2, Play, Pause, Download } from 'lucide-react';

export default function StoryCreator({ projectId, onStoryCreated, generatedStory, onStoryGenerated }: { projectId: string; onStoryCreated?: () => void; generatedStory?: any; onStoryGenerated?: (story: any) => void }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [story, setStory] = useState<any>(generatedStory || null);
  const [playingAudio, setPlayingAudio] = useState<{[key: string]: boolean}>({});
  const [audioPlayer, setAudioPlayer] = useState<{[key: string]: HTMLAudioElement}>({});

  // Sync parent story state when it changes
  useEffect(() => {
    if (generatedStory) {
      setStory(generatedStory);
    }
  }, [generatedStory]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await api.createStory(projectId, prompt);
      setStory(result);
      // Persist story to parent state
      if (onStoryGenerated) {
        onStoryGenerated(result);
      }
      // Callback to refresh project data
      if (onStoryCreated) {
        onStoryCreated();
      }
    } catch (error) {
      alert('Failed to generate story');
    }
    setLoading(false);
  };

  const handlePlayPause = (sceneId: string, audioFilename: string) => {
    if (playingAudio[sceneId]) {
      // Pause
      const player = audioPlayer[sceneId];
      if (player) {
        player.pause();
      }
      setPlayingAudio({ ...playingAudio, [sceneId]: false });
    } else {
      // Play
      const audio = new Audio(`http://localhost:5000/api/audio/${audioFilename}`);
      audio.onended = () => {
        setPlayingAudio({ ...playingAudio, [sceneId]: false });
      };
      audio.play();
      setAudioPlayer({ ...audioPlayer, [sceneId]: audio });
      setPlayingAudio({ ...playingAudio, [sceneId]: true });
    }
  };

  const handleDownload = (audioFilename: string, sceneTitle: string) => {
    const link = document.createElement('a');
    link.href = `http://localhost:5000/api/audio/${audioFilename}`;
    link.download = `${sceneTitle}.wav`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleGenerate} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Story Prompt</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe your story... e.g., 'A brave little rabbit finds a magical forest'"
            rows={6}
          />
        </div>
        <button
          type="submit"
          disabled={loading || !prompt}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <Wand2 size={20} /> {loading ? 'Generating...' : 'Generate Story'}
        </button>
      </form>

      {story && (
        <div className="bg-green-50 rounded-lg p-4 border border-green-200">
          <h3 className="font-bold mb-3 text-green-900">✅ Story Generated - Narration & Audio Auto-Created!</h3>
          <div className="space-y-3 text-sm">
            {story.scenes?.map((scene: any, idx: number) => {
              const audioFilename = scene.audio_filename || `narration_${scene.id}.wav`;
              return (
                <div key={idx} className="bg-white p-3 rounded border border-green-200">
                  <div className="font-bold text-green-700">Scene {scene.sequence}: {scene.title}</div>
                  <div className="text-gray-700 mt-2">
                    <strong>Narration:</strong> {scene.narration}
                  </div>
                  <div className="mt-3 flex items-center gap-2">
                    <button
                      onClick={() => handlePlayPause(scene.id, audioFilename)}
                      className={`flex items-center gap-1 px-3 py-1 rounded text-sm transition ${
                        playingAudio[scene.id]
                          ? 'bg-red-500 text-white hover:bg-red-600'
                          : 'bg-blue-500 text-white hover:bg-blue-600'
                      }`}
                    >
                      {playingAudio[scene.id] ? (
                        <>
                          <Pause size={14} /> Pause
                        </>
                      ) : (
                        <>
                          <Play size={14} /> Play Audio
                        </>
                      )}
                    </button>
                    <button
                      onClick={() => handleDownload(audioFilename, scene.title)}
                      className="flex items-center gap-1 px-3 py-1 rounded text-sm bg-green-600 text-white hover:bg-green-700 transition"
                    >
                      <Download size={14} /> Download
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
          <p className="text-xs text-gray-600 mt-3">
            💡 All narration and audio have been automatically generated. Go to the "Edit" tab to customize or view the scenes.
          </p>
        </div>
      )}
    </div>
  );
}
