/**
 * Centralized color palette for business dashboards
 * Based on color psychology for different business domains
 */

export const chartColors = {
  // Revenue & Sales (Green = Growth, Success)
  revenue: {
    primary: '#10B981',
    secondary: '#059669',
    gradient: ['#10B981', '#059669'],
    light: '#D1FAE5',
    text: '#065F46',
  },
  
  // Expenses & Costs (Red = Caution, Control)
  expenses: {
    primary: '#EF4444',
    secondary: '#DC2626',
    gradient: ['#EF4444', '#DC2626'],
    light: '#FEE2E2',
    text: '#991B1B',
  },
  
  // Profit & Margins (Blue = Trust, Stability)
  profit: {
    primary: '#3B82F6',
    secondary: '#2563EB',
    gradient: ['#3B82F6', '#2563EB'],
    light: '#DBEAFE',
    text: '#1E40AF',
  },
  
  // Operations & Efficiency (Orange = Energy, Action)
  operations: {
    primary: '#F59E0B',
    secondary: '#D97706',
    gradient: ['#F59E0B', '#D97706'],
    light: '#FEF3C7',
    text: '#92400E',
  },
  
  // HR & People (Purple = Creativity, Team)
  people: {
    primary: '#8B5CF6',
    secondary: '#7C3AED',
    gradient: ['#8B5CF6', '#7C3AED'],
    light: '#EDE9FE',
    text: '#5B21B6',
  },
  
  // Finance & Wealth (Indigo = Premium, Wealth)
  finance: {
    primary: '#6366F1',
    secondary: '#4F46E5',
    gradient: ['#6366F1', '#4F46E5'],
    light: '#E0E7FF',
    text: '#3730A3',
  },
  
  // Alerts & Risks (Amber = Warning, Attention)
  alerts: {
    primary: '#F59E0B',
    secondary: '#DC2626',
    gradient: ['#F59E0B', '#DC2626'],
    light: '#FEF3C7',
    text: '#92400E',
  },
  
  // Neutral & Background
  neutral: {
    primary: '#6B7280',
    secondary: '#4B5563',
    gradient: ['#6B7280', '#4B5563'],
    light: '#F3F4F6',
    text: '#1F2937',
  },
};

/**
 * Multi-color palette for category charts (donut, pie, etc.)
 */
export const categoryColors = [
  '#3B82F6', // Blue
  '#10B981', // Green
  '#F59E0B', // Orange
  '#8B5CF6', // Purple
  '#EF4444', // Red
  '#06B6D4', // Cyan
  '#EC4899', // Pink
  '#14B8A6', // Teal
  '#F97316', // Orange (darker)
  '#6366F1', // Indigo
];

/**
 * Get color by index for category charts
 */
export const getCategoryColor = (index: number): string => {
  return categoryColors[index % categoryColors.length];
};

/**
 * Generate gradient CSS for metric cards
 */
export const getGradientStyle = (colors: string[]) => {
  return {
    background: `linear-gradient(135deg, ${colors[0]} 0%, ${colors[1]} 100%)`,
  };
};

/**
 * Chart theme configuration
 */
export const chartTheme = {
  grid: {
    stroke: '#E5E7EB',
    strokeDasharray: '3 3',
  },
  axis: {
    stroke: '#9CA3AF',
    fontSize: 12,
    fill: '#6B7280',
  },
  tooltip: {
    background: '#1F2937',
    border: 'none',
    borderRadius: '8px',
    padding: '12px',
    color: '#FFFFFF',
    fontSize: '14px',
    fontWeight: '500',
  },
  legend: {
    fontSize: 12,
    fill: '#6B7280',
  },
};
