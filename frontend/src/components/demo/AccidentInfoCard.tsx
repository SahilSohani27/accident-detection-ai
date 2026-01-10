import { AlertTriangle, Target, Hash, MapPin } from 'lucide-react';
import { AccidentInfo } from '@/services/api';

interface AccidentInfoCardProps {
  accidentInfo: AccidentInfo;
}

const AccidentInfoCard = ({ accidentInfo }: AccidentInfoCardProps) => {
  const confidencePercent = (accidentInfo.confidence * 100).toFixed(1);

  return (
    <div className="p-6 rounded-xl bg-card border-2 border-emergency/50 glow-emergency">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-full bg-emergency/20 flex items-center justify-center pulse-emergency">
          <AlertTriangle className="w-6 h-6 text-emergency" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-emergency">🚨 Accident Detected</h3>
          <p className="text-sm text-muted-foreground">Analysis complete</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {/* Confidence */}
        <div className="p-4 rounded-lg bg-secondary/50">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-4 h-4 text-emergency" />
            <span className="text-xs text-muted-foreground">Confidence</span>
          </div>
          <div className="text-2xl font-bold text-emergency">{confidencePercent}%</div>
        </div>

        {/* Frame Index */}
        <div className="p-4 rounded-lg bg-secondary/50">
          <div className="flex items-center gap-2 mb-2">
            <Hash className="w-4 h-4 text-warning" />
            <span className="text-xs text-muted-foreground">Frame</span>
          </div>
          <div className="text-2xl font-bold text-warning">#{accidentInfo.frame_idx}</div>
        </div>

        {/* Coordinates */}
        <div className="p-4 rounded-lg bg-secondary/50">
          <div className="flex items-center gap-2 mb-2">
            <MapPin className="w-4 h-4 text-blue-500" />
            <span className="text-xs text-muted-foreground">Bounding Box</span>
          </div>
          <div className="text-xs font-mono text-muted-foreground">
            [{accidentInfo.coordinates.map(c => c.toFixed(0)).join(', ')}]
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccidentInfoCard;
