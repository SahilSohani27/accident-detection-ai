import { MessageSquare } from 'lucide-react';

interface SOSMessageProps {
  message: string;
}

const SOSMessage = ({ message }: SOSMessageProps) => {
  return (
    <div className="p-6 rounded-xl bg-card border border-border">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <MessageSquare className="w-5 h-5 text-emergency" />
        Generated SOS Message
      </h3>
      <div className="p-4 rounded-lg bg-secondary/50 border border-border">
        <p className="text-sm text-foreground whitespace-pre-wrap font-mono leading-relaxed">
          {message}
        </p>
      </div>
    </div>
  );
};

export default SOSMessage;
