import HeroSection from '@/components/landing/HeroSection';
import ProblemSection from '@/components/landing/ProblemSection';
import SolutionSection from '@/components/landing/SolutionSection';
import ArchitectureSection from '@/components/landing/ArchitectureSection';
import TechStackSection from '@/components/landing/TechStackSection';
import Footer from '@/components/landing/Footer';

const LandingPage = () => {
  return (
    <main className="min-h-screen bg-background">
      <HeroSection />
      <ProblemSection />
      <SolutionSection />
      <ArchitectureSection />
      <TechStackSection />
      <Footer />
    </main>
  );
};

export default LandingPage;
