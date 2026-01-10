import { getMediaUrl } from '@/services/api';

interface FramePreviewProps {
  frameUrl: string;
}

const FramePreview = ({ frameUrl }: FramePreviewProps) => {
  const fullUrl = getMediaUrl(frameUrl);

  return (
    <div className="p-6 rounded-xl bg-card border border-border">
      <h3 className="text-lg font-semibold mb-4">📸 Best Detection Frame</h3>
      <div className="relative rounded-lg overflow-hidden bg-black">
        <img
          src={fullUrl}
          alt="Best detection frame"
          className="w-full aspect-video object-contain"
        />
      </div>
      <p className="text-xs text-muted-foreground mt-2 text-center">
        Frame with highest detection confidence
      </p>
    </div>
  );
};

export default FramePreview;
