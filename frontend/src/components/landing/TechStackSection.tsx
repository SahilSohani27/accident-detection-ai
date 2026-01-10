const technologies = [
  { name: "FastAPI", description: "High-performance Python backend" },
  { name: "YOLOv8", description: "State-of-the-art object detection" },
  { name: "OpenCV", description: "Computer vision processing" },
  { name: "OpenAI GPT", description: "Intelligent SOS generation" },
  { name: "Telegram Bot", description: "Instant alert delivery" },
  { name: "React + Tailwind", description: "Modern responsive UI" },
];

const TechStackSection = () => {
  return (
    <section className="py-24">
      <div className="container px-4">
        <div className="max-w-4xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Tech <span className="text-emergency">Stack</span>
            </h2>
            <p className="text-muted-foreground text-lg">
              Built with industry-leading technologies
            </p>
          </div>

          {/* Tech grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {technologies.map((tech, index) => (
              <div
                key={index}
                className="group p-5 rounded-xl bg-card border border-border hover:border-emergency/50 transition-all duration-300"
              >
                <h3 className="text-lg font-semibold mb-1 group-hover:text-emergency transition-colors">
                  {tech.name}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {tech.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechStackSection;
