import { Upload, Cpu, Filter, Film, MessageSquare, Send, ArrowRight } from 'lucide-react';

const steps = [
  {
    icon: Upload,
    title: "Upload Video",
    description: "Upload CCTV or dashcam footage"
  },
  {
    icon: Cpu,
    title: "AI Detection",
    description: "YOLOv8 analyzes each frame"
  },
  {
    icon: Filter,
    title: "Validation",
    description: "Frame streak logic reduces false positives"
  },
  {
    icon: Film,
    title: "Clip Generation",
    description: "10-second accident clip extracted"
  },
  {
    icon: MessageSquare,
    title: "SOS Message",
    description: "GPT generates emergency alert"
  },
  {
    icon: Send,
    title: "Telegram Alert",
    description: "Instant notification to responders"
  }
];

const SolutionSection = () => {
  return (
    <section className="py-24">
      <div className="container px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              How It <span className="text-emergency">Works</span>
            </h2>
            <p className="text-muted-foreground text-lg">
              From video upload to emergency response in seconds
            </p>
          </div>

          {/* Step flow */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {steps.map((step, index) => (
              <div key={index} className="relative">
                <div className="flex flex-col items-center text-center group">
                  {/* Step number */}
                  <div className="absolute -top-3 -left-1 w-6 h-6 rounded-full bg-emergency text-emergency-foreground text-xs font-bold flex items-center justify-center z-10">
                    {index + 1}
                  </div>
                  
                  {/* Icon container */}
                  <div className="w-16 h-16 rounded-xl bg-card border border-border flex items-center justify-center mb-3 group-hover:border-emergency/50 group-hover:bg-emergency/5 transition-all duration-300">
                    <step.icon className="w-7 h-7 text-emergency" />
                  </div>
                  
                  {/* Text */}
                  <h3 className="text-sm font-semibold mb-1">{step.title}</h3>
                  <p className="text-xs text-muted-foreground">{step.description}</p>
                </div>

                {/* Connector arrow (not on last item) */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-8 -right-2 text-muted-foreground/30">
                    <ArrowRight className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default SolutionSection;
