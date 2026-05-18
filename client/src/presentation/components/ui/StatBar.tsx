import { cn } from './cn';

interface Props {
  label: string;
  current: number;
  max: number;
  icon: React.ReactNode;
  barClass: string;
  iconBgClass: string;
}

export function StatBar({ label, current, max, icon, barClass, iconBgClass }: Props) {
  const percent = Math.round((current / max) * 100);
  return (
    <div className="flex items-center gap-3 p-2 bg-background/50 border-2 border-primary/30">
      <div className={cn('w-8 h-8 border flex items-center justify-center', iconBgClass)}>
        {icon}
      </div>
      <div className="flex-1">
        <div className="text-xs text-muted-foreground mb-1">{label}</div>
        <div className="h-2 bg-secondary border border-primary/50 overflow-hidden">
          <div className={cn('h-full transition-all duration-500', barClass)} style={{ width: `${percent}%` }} />
        </div>
      </div>
      <span className="text-sm text-gold">{current}/{max}</span>
    </div>
  );
}
