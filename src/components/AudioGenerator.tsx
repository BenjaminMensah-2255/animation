'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { Volume2, Play, Pause, Download } from 'lucide-react';

export default function AudioGenerator({
  projectId,
  sceneId,
  text
}: {
  projectId: string;
  sceneId: string;
  text: string;
}) {
  const [loading, setLoading] = useState(false);
  const [duration, setDuration] = useState<number | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioElement, setAudioElement] = useState<HTMLAudioElement | null>(null);

  const handleGenerateAudio = async () => {
    if (!text || text.trim() === '') {
      alert('Please add narration text above to generate audio');
      return;
    }

    setLoading(true);
    try {
      // Estimate duration first
      const durResult = await api.estimateDuration(text);
      setDuration(durResult.estimated_duration);

      // Generate audio
      const result = await api.generateAudio(projectId, text, 'narration', sceneId);
      if (result.filename) {
        // Use the full filename with .wav extension
        const audioFilename = result.filename.includes('.wav') ? result.filename : `${result.filename}.wav`;
        const url = `http://localhost:5000/api/audio/${audioFilename}`;
        setAudioUrl(url);
        alert('Audio generated successfully!');
      }
    } catch (error) {
      alert('Failed to generate audio');
    }
    setLoading(false);
  };

  const handlePlayPause = () => {
    if (!audioUrl) return;

    if (!audioElement) {
      const audio = new Audio(audioUrl);
      audio.onended = () => setIsPlaying(false);
      setAudioElement(audio);
      audio.play();
      setIsPlaying(true);
    } else {
      if (isPlaying) {
        audioElement.pause();
        setIsPlaying(false);
      } else {
        audioElement.play();
        setIsPlaying(true);
      }
    }
  };

  const handleDownload = () => {
    if (!audioUrl) return;
    const link = document.createElement('a');
    link.href = audioUrl;
    link.download = `audio-${sceneId}.wav`;
    link.click();
  };

  return (
    <div className="space-y-3">
      <div className="bg-blue-50 p-3 rounded border border-blue-200">
        <p className="text-sm text-gray-700">
          {text ? `Text: "${text.substring(0, 60)}..."` : 'Add narration text above to generate audio'}
        </p>
        {duration && <p className="text-xs text-gray-600 mt-1">Estimated duration: {duration.toFixed(1)}s</p>}
      </div>

      <button
        onClick={handleGenerateAudio}
        disabled={loading || !text}
        className={`w-full py-2 rounded-lg flex items-center justify-center gap-2 font-medium transition-all ${
          loading || !text
            ? 'bg-gray-400 text-white cursor-not-allowed opacity-50'
            : 'bg-purple-600 text-white hover:bg-purple-700'
        }`}
        title={!text ? 'Add narration text to generate audio' : 'Click to generate audio'}
      >
        <Volume2 size={16} /> {loading ? 'Generating...' : 'Generate Audio'}
      </button>

      {audioUrl && (
        <div className="bg-green-50 p-4 rounded border border-green-200 space-y-3">
          <p className="text-sm font-medium text-green-700">✓ Audio generated</p>
          
          <div className="flex gap-2">
            <button
              onClick={handlePlayPause}
              className="flex-1 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 flex items-center justify-center gap-2"
            >
              {isPlaying ? (
                <>
                  <Pause size={16} /> Pause
                </>
              ) : (
                <>
                  <Play size={16} /> Play Audio
                </>
              )}
            </button>
            
            <button
              onClick={handleDownload}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center justify-center"
              title="Download audio file"
            >
              <Download size={16} />
            </button>
          </div>

          <div className="text-xs text-gray-600">
            Duration: {duration ? `${duration.toFixed(1)}s` : 'calculating...'}
          </div>
        </div>
      )}
    </div>
  );
}
