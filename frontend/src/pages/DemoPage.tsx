import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import VideoInputPanel from '@/components/demo/VideoInputPanel';
import ResultsPanel from '@/components/demo/ResultsPanel';
import { uploadVideo, AccidentDetectionResponse } from '@/services/api';

const DemoPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [result, setResult] = useState<AccidentDetectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleVideoSelect = (file: File) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
    setCurrentStep(0);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setError(null);
    setResult(null);
    setCurrentStep(1); // Start with step 1: Uploading

    // Simulate step progression while processing
    // Steps: 1=Uploading, 2=Analyzing, 3=Detecting, 4=Generating SOS, 5=Sending Alert, 6=Complete
    const stepInterval = setInterval(() => {
      setCurrentStep(prev => {
        if (prev < 5) return prev + 1; // Progress through steps 1-5
        return prev;
      });
    }, 2000); // Update every 2 seconds

    try {
      console.log(`Uploading video: ${selectedFile.name}`);
      const response = await uploadVideo(selectedFile);
      
      clearInterval(stepInterval);
      setCurrentStep(6); // Mark as complete
      
      console.log('Video processing completed:', response);
      setResult(response);
    } catch (err) {
      clearInterval(stepInterval);
      const errorMessage = err instanceof Error ? err.message : 'Failed to process video. Ensure the backend is running.';
      console.error('Error processing video:', err);
      setError(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container px-4 py-4 flex items-center justify-between">
          <Link to="/">
            <Button variant="ghost" size="sm" className="gap-2">
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Button>
          </Link>
          <h1 className="text-lg font-bold">
            🚨 <span className="text-emergency">ResQ</span> Dashboard
          </h1>
          <div className="w-24" />
        </div>
      </header>

      {/* Main Content */}
      <div className="container px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - Video Input */}
          <div>
            <h2 className="text-2xl font-bold mb-6">Video Input</h2>
            <VideoInputPanel
              onVideoSelect={handleVideoSelect}
              isProcessing={isProcessing}
              onAnalyze={handleAnalyze}
              hasVideo={selectedFile !== null}
            />
            {selectedFile && (
              <p className="mt-4 text-sm text-muted-foreground">
                Selected: <span className="text-foreground font-medium">{selectedFile.name}</span>
              </p>
            )}
          </div>

          {/* Right Panel - Results */}
          <div>
            <h2 className="text-2xl font-bold mb-6">Analysis Results</h2>
            <ResultsPanel
              isProcessing={isProcessing}
              currentStep={currentStep}
              result={result}
              error={error}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoPage;
