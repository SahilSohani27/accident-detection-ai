import { getMediaUrl } from '@/services/api';

interface VideoPlayerProps {
  clipUrl: string;
}

const VideoPlayer = ({ clipUrl }: VideoPlayerProps) => {
  const fullUrl = getMediaUrl(clipUrl);

  return (
    <div className="p-6 rounded-xl bg-card border border-border">
      <h3 className="text-lg font-semibold mb-4">🎬 Accident Clip</h3>
      <div className="relative rounded-lg overflow-hidden bg-black">
        <video
          src={fullUrl}
          autoPlay
          loop
          muted
          controls
          playsInline
          className="w-full aspect-video object-contain"
        >
          Your browser does not support the video tag.
        </video>
      </div>
      <p className="text-xs text-muted-foreground mt-2 text-center">
        10-second extracted accident clip (loops automatically)
      </p>
    </div>
  );
};

export default VideoPlayer;
