import { Clock, Eye, Radio } from 'lucide-react';

const problems = [
  {
    icon: Clock,
    title: "Delay in Response",
    description: "Every minute of delay in accident response significantly reduces survival rates and increases the severity of injuries."
  },
  {
    icon: Eye,
    title: "Unreliable Monitoring",
    description: "Manual monitoring of CCTV feeds is prone to human error, fatigue, and cannot scale to cover all road networks effectively."
  },
  {
    icon: Radio,
    title: "Lack of Intelligence",
    description: "Emergency services lack real-time intelligence about accident severity, location, and conditions to optimize response strategies."
  }
];

const ProblemSection = () => {
  return (
    <section className="py-24 bg-secondary/30">
      <div className="container px-4">
        <div className="max-w-4xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why This <span className="text-emergency">Matters</span>
            </h2>
            <p className="text-muted-foreground text-lg">
              Traditional accident response systems are failing to save lives
            </p>
          </div>

          {/* Problem cards */}
          <div className="grid md:grid-cols-3 gap-6">
            {problems.map((problem, index) => (
              <div 
                key={index}
                className="group p-6 rounded-xl bg-card border border-border hover:border-emergency/50 transition-all duration-300 card-glow"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="w-12 h-12 rounded-lg bg-emergency/10 flex items-center justify-center mb-4 group-hover:bg-emergency/20 transition-colors">
                  <problem.icon className="w-6 h-6 text-emergency" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{problem.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {problem.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProblemSection;
