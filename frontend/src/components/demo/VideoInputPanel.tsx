import { useRef } from 'react';
import { Upload, Video, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import highwayVideo from '../Testing/test4.mp4';

// ============================================================================
// DEMO VIDEO PATHS - UPDATE THESE WITH YOUR ACTUAL VIDEO FILE PATHS
// Place your demo videos in the public folder and update the paths below
// ============================================================================
const DEMO_VIDEOS = {
  highway: '/demo-videos/highway-accident.mp4',        // TODO: Add your highway accident video
  intersection: '/demo-videos/vehicle-out-of-control.mp4', // TODO: Add your intersection crash video
  nighttime: '/demo-videos/nighttime-collision.mp4',   // TODO: Add your night-time collision video
};
// ============================================================================

interface VideoInputPanelProps {
  onVideoSelect: (file: File) => void;
  isProcessing: boolean;
  onAnalyze: () => void;
  hasVideo: boolean;
}

const VideoInputPanel = ({ onVideoSelect, isProcessing, onAnalyze, hasVideo }: VideoInputPanelProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDemoVideoSelect = async (videoPath: string) => {
    try {
      const response = await fetch(videoPath);
      const blob = await response.blob();
      const fileName = videoPath.split('/').pop() || 'demo-video.mp4';
      const file = new File([blob], fileName, { type: 'video/mp4' });
      onVideoSelect(file);
    } catch (error) {
      console.error('Error loading demo video:', error);
      alert('Demo video not found. Please ensure the video file exists at: ' + videoPath);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      const validTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/x-msvideo', 'video/quicktime', 'video/x-matroska'];
      if (!validTypes.some(type => file.type.includes(type.split('/')[1]))) {
        alert('Please upload a valid video file (mp4, avi, mov, mkv)');
        return;
      }
      // Validate file size (50MB max)
      if (file.size > 50 * 1024 * 1024) {
        alert('File size must be less than 50MB');
        return;
      }
      onVideoSelect(file);
    }
  };

  return (
    <div className="space-y-6">
      {/* Section 1: Sample Videos */}
      <div className="p-6 rounded-xl bg-card border border-border">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Video className="w-5 h-5 text-emergency" />
          Sample Videos
        </h3>
        <p className="text-sm text-muted-foreground mb-4">
          Click to load a pre-recorded demo video for testing
        </p>
        <div className="grid gap-3">
          <Button
            variant="outline"
            size="lg"
            className="w-full justify-start text-left h-auto py-4 hover:border-emergency/50 hover:bg-emergency/5"
            onClick={() => handleDemoVideoSelect(DEMO_VIDEOS.highway)}
            disabled={isProcessing}
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-emergency/10 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-emergency" />
              </div>
              <div>
                <div className="font-medium">Highway Accident</div>
                <div className="text-xs text-muted-foreground">Multi-lane highway collision</div>
              </div>
            </div>
          </Button>

          <Button
            variant="outline"
            size="lg"
            className="w-full justify-start text-left h-auto py-4 hover:border-emergency/50 hover:bg-emergency/5"
            onClick={() => handleDemoVideoSelect(DEMO_VIDEOS.intersection)}
            disabled={isProcessing}
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-warning/10 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-warning" />
              </div>
              <div>
                <div className="font-medium">Vehicle Out of Control</div>
                <div className="text-xs text-muted-foreground">Vehicle veers off roadway</div>
              </div>
            </div>
          </Button>

          <Button
            variant="outline"
            size="lg"
            className="w-full justify-start text-left h-auto py-4 hover:border-emergency/50 hover:bg-emergency/5"
            onClick={() => handleDemoVideoSelect(DEMO_VIDEOS.nighttime)}
            disabled={isProcessing}
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-blue-500" />
              </div>
              <div>
                <div className="font-medium">Night-Time Collision</div>
                <div className="text-xs text-muted-foreground">Low-light conditions</div>
              </div>
            </div>
          </Button>
        </div>
      </div>

      {/* Section 2: Upload Custom Video */}
      <div className="p-6 rounded-xl bg-card border border-border">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Upload className="w-5 h-5 text-emergency" />
          Upload Custom Video
        </h3>
        <div
          className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:border-emergency/50 transition-colors cursor-pointer"
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className="w-10 h-10 text-muted-foreground mx-auto mb-3" />
          <p className="text-sm text-muted-foreground mb-2">
            Click to upload or drag and drop
          </p>
          <p className="text-xs text-muted-foreground">
            MP4, AVI, MOV, MKV (Max 50MB)
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".mp4,.avi,.mov,.mkv,video/mp4,video/avi,video/quicktime,video/x-matroska"
            className="hidden"
            onChange={handleFileChange}
            disabled={isProcessing}
          />
        </div>
      </div>

      {/* Analyze Button */}
      <Button
        size="lg"
        className="w-full bg-emergency hover:bg-emergency/90 text-emergency-foreground text-lg py-6 glow-emergency disabled:opacity-50 disabled:cursor-not-allowed"
        onClick={onAnalyze}
        disabled={!hasVideo || isProcessing}
      >
        {isProcessing ? (
          <>
            <div className="w-5 h-5 border-2 border-emergency-foreground border-t-transparent rounded-full animate-spin mr-2" />
            Processing...
          </>
        ) : (
          <>
            Analyze Video
            <AlertTriangle className="w-5 h-5 ml-2" />
          </>
        )}
      </Button>
    </div>
  );
};

export default VideoInputPanel;
