import axios from 'axios';

// Configure the base URL - can be overridden via environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for video processing
});

export interface AccidentInfo {
  confidence: number;
  frame_idx: number;
  coordinates: number[];
}

export interface AccidentDetectionResponse {
  accident_info?: AccidentInfo;
  clip_url?: string;
  frame_url?: string;
  sos_message?: string;
  telegram?: string;
  message?: string;
}

export const uploadVideo = async (file: File): Promise<AccidentDetectionResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await apiClient.post('/upload-video/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      },
    });

    // Map backend response to frontend expected format
    const data = response.data;
    return {
      accident_info: data.accident_info,
      clip_url: data.clip_url || (data.clip_path ? getMediaUrl(data.clip_path) : undefined),
      frame_url: data.frame_url || (data.best_frame ? getMediaUrl(data.best_frame) : undefined),
      sos_message: data.sos_message,
      telegram: data.telegram,
      message: data.message,
    };
  } catch (error: any) {
    // Handle error responses
    if (error.response) {
      const errorMessage = error.response.data?.detail || error.response.data?.message || 'Failed to process video';
      throw new Error(errorMessage);
    }
    throw error;
  }
};

// Helper to get full URL for media files
export const getMediaUrl = (path: string): string => {
  if (!path) return '';
  if (path.startsWith('http')) {
    return path;
  }
  // If path is relative, prepend API base URL
  if (path.startsWith('/')) {
    return `${API_BASE_URL}${path}`;
  }
  // If path is a filename, assume it's in the static folder
  return `${API_BASE_URL}/static/${path}`;
};

export default apiClient;
