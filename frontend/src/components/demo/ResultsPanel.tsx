import { AccidentDetectionResponse } from '@/services/api';
import StepIndicator from './StepIndicator';
import AccidentInfoCard from './AccidentInfoCard';
import VideoPlayer from './VideoPlayer';
import FramePreview from './FramePreview';
import SOSMessage from './SOSMessage';
import TelegramStatus from './TelegramStatus';
import { AlertCircle, CheckCircle } from 'lucide-react';

interface ResultsPanelProps {
  isProcessing: boolean;
  currentStep: number;
  result: AccidentDetectionResponse | null;
  error: string | null;
}

const ResultsPanel = ({ isProcessing, currentStep, result, error }: ResultsPanelProps) => {
  const hasAccident = result?.accident_info !== undefined;

  return (
    <div className="space-y-6">
      {/* Step Indicator - Always show during processing */}
      {(isProcessing || result) && (
        <StepIndicator 
          currentStep={currentStep} 
          isComplete={!isProcessing && result !== null} 
        />
      )}

      {/* Error State */}
      {error && (
        <div className="p-6 rounded-xl bg-destructive/10 border border-destructive/30">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-6 h-6 text-destructive" />
            <div>
              <h3 className="font-semibold text-destructive">Error Processing Video</h3>
              <p className="text-sm text-muted-foreground">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results - Only show when not processing and we have results */}
      {!isProcessing && result && (
        <>
          {hasAccident ? (
            <>
              {/* Accident Detected Results */}
              <AccidentInfoCard accidentInfo={result.accident_info!} />
              
              {result.sos_message && (
                <SOSMessage message={result.sos_message} />
              )}
              
              {result.telegram && (
                <TelegramStatus status={result.telegram} />
              )}
              
              {result.clip_url && (
                <VideoPlayer clipUrl={result.clip_url} />
              )}
              
              {result.frame_url && (
                <FramePreview frameUrl={result.frame_url} />
              )}
            </>
          ) : (
            /* No Accident Detected */
            <div className="p-6 rounded-xl bg-success/10 border border-success/30">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-success/20 flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-success" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-success">No Accident Detected</h3>
                  <p className="text-sm text-muted-foreground">
                    {result.message || 'The video was analyzed and no accidents were found.'}
                  </p>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* Empty State */}
      {!isProcessing && !result && !error && (
        <div className="p-12 rounded-xl bg-card border border-border border-dashed text-center">
          <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
            <AlertCircle className="w-8 h-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold mb-2">No Video Analyzed</h3>
          <p className="text-sm text-muted-foreground">
            Select a sample video or upload your own to begin analysis
          </p>
        </div>
      )}
    </div>
  );
};

export default ResultsPanel;
