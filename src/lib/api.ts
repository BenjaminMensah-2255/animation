const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export const api = {
  // Projects
  createProject: (name: string, description: string) =>
    fetch(`${API_BASE}/projects/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description })
    }).then(r => r.json()),

  getProject: (projectId: string) =>
    fetch(`${API_BASE}/projects/${projectId}`).then(r => r.json()),

  listProjects: () =>
    fetch(`${API_BASE}/projects`).then(r => r.json()),

  updateProject: (projectId: string, data: any) =>
    fetch(`${API_BASE}/projects/${projectId}/update`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => r.json()),

  deleteProject: (projectId: string) =>
    fetch(`${API_BASE}/projects/${projectId}/delete`, { method: 'DELETE' }).then(r => r.json()),

  // Stories
  createStory: (projectId: string, prompt: string) =>
    fetch(`${API_BASE}/stories/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId, prompt })
    }).then(r => r.json()),

  getCharacters: () =>
    fetch(`${API_BASE}/stories/characters`).then(r => r.json()),

  getBackgrounds: () =>
    fetch(`${API_BASE}/stories/backgrounds`).then(r => r.json()),

  // Scenes
  createScene: (projectId: string, sceneData: any) =>
    fetch(`${API_BASE}/projects/${projectId}/scenes/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sceneData)
    }).then(r => r.json()),

  updateScene: (sceneId: string, sceneData: any) =>
    fetch(`${API_BASE}/animations/scenes/${sceneId}/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sceneData)
    }).then(r => r.json()),

  deleteScene: (sceneId: string) =>
    fetch(`${API_BASE}/animations/scenes/${sceneId}/delete`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    }).then(r => r.json()),

  // Animations
  previewScene: (sceneId: string) =>
    fetch(`${API_BASE}/animations/preview/${sceneId}`).then(r => r.text()),

  renderAnimation: (projectId: string) =>
    fetch(`${API_BASE}/animations/render`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId })
    }).then(r => r.json()),

  exportVideo: (projectId: string) =>
    fetch(`${API_BASE}/animations/export/${projectId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }).then(r => r.json()),

  // Audio
  generateAudio: (projectId: string, text: string, trackType: string = 'narration', sceneId?: string) =>
    fetch(`${API_BASE}/audio/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId, text, track_type: trackType, scene_id: sceneId })
    }).then(r => r.json()),

  estimateDuration: (text: string) =>
    fetch(`${API_BASE}/audio/estimate-duration`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    }).then(r => r.json()),

  getMouthAnimation: (duration: number) =>
    fetch(`${API_BASE}/audio/mouth-animation/${duration}`).then(r => r.json())
};
