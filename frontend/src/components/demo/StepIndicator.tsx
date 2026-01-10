import { Check, Loader2 } from 'lucide-react';

const steps = [
  { id: 1, label: 'Uploading Video' },
  { id: 2, label: 'Processing Video' },
  { id: 3, label: 'Accident Detection' },
  { id: 4, label: 'Clipping Accident' },
  { id: 5, label: 'Generating SOS Message' },
  { id: 6, label: 'Sending Telegram Alert' },
];

interface StepIndicatorProps {
  currentStep: number;
  isComplete: boolean;
}

const StepIndicator = ({ currentStep, isComplete }: StepIndicatorProps) => {
  return (
    <div className="p-6 rounded-xl bg-card border border-border">
      <h3 className="text-lg font-semibold mb-6">Processing Steps</h3>
      
      <div className="space-y-3">
        {steps.map((step) => {
          const isCompleted = isComplete || step.id < currentStep;
          const isActive = !isComplete && step.id === currentStep;
          const isPending = !isComplete && step.id > currentStep;

          return (
            <div
              key={step.id}
              className={`flex items-center gap-4 p-3 rounded-lg transition-all duration-300 ${
                isCompleted
                  ? 'bg-success/10 border border-success/30'
                  : isActive
                  ? 'bg-emergency/10 border border-emergency/30 animate-step-pulse'
                  : 'bg-secondary/30 border border-transparent'
              }`}
            >
              {/* Step indicator circle */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 ${
                  isCompleted
                    ? 'bg-success text-success-foreground'
                    : isActive
                    ? 'bg-emergency text-emergency-foreground'
                    : 'bg-muted text-muted-foreground'
                }`}
              >
                {isCompleted ? (
                  <Check className="w-4 h-4" />
                ) : isActive ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  step.id
                )}
              </div>

              {/* Step label */}
              <span
                className={`text-sm font-medium transition-colors ${
                  isCompleted
                    ? 'text-success'
                    : isActive
                    ? 'text-emergency'
                    : 'text-muted-foreground'
                }`}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StepIndicator;
