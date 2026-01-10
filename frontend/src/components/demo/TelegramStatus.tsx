import { Send, CheckCircle, XCircle } from 'lucide-react';

interface TelegramStatusProps {
  status: string;
}

const TelegramStatus = ({ status }: TelegramStatusProps) => {
  const isSuccess = status.toLowerCase().includes('sent') || status.toLowerCase().includes('success');

  return (
    <div className="p-6 rounded-xl bg-card border border-border">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Send className="w-5 h-5 text-blue-500" />
        Telegram Alert Status
      </h3>
      <div className={`p-4 rounded-lg flex items-center gap-3 ${
        isSuccess 
          ? 'bg-success/10 border border-success/30' 
          : 'bg-destructive/10 border border-destructive/30'
      }`}>
        {isSuccess ? (
          <CheckCircle className="w-6 h-6 text-success flex-shrink-0" />
        ) : (
          <XCircle className="w-6 h-6 text-destructive flex-shrink-0" />
        )}
        <span className={`text-sm font-medium ${isSuccess ? 'text-success' : 'text-destructive'}`}>
          {status}
        </span>
      </div>
    </div>
  );
};

export default TelegramStatus;
