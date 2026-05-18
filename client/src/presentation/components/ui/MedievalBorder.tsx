import { cn } from './cn';

interface Props {
  children: React.ReactNode;
  className?: string;
  goldCorners?: boolean;
}

export function MedievalBorder({ children, className, goldCorners = false }: Props) {
  const cornerColor = goldCorners ? 'border-gold' : 'border-primary';
  return (
    <div className={cn('relative', className)}>
      <div className={cn('absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4', cornerColor)} />
      <div className={cn('absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4', cornerColor)} />
      <div className={cn('absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4', cornerColor)} />
      <div className={cn('absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4', cornerColor)} />
      {children}
    </div>
  );
}
