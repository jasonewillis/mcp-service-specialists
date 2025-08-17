"""
Frontend UX Agent

This agent specializes in Next.js/React development, UI/UX optimization,
and accessibility compliance for the Fed Job Advisor platform.
"""

from typing import Dict, Any, List, Optional
from langchain.tools import Tool
import structlog
import json
import re

from app.agents.base import FederalJobAgent, AgentConfig, AgentResponse

logger = structlog.get_logger()


class FrontendUXAgent(FederalJobAgent):
    """
    Specialized agent for frontend development and user experience
    
    Focuses on:
    - React component generation and optimization
    - Next.js 14 App Router best practices
    - TypeScript type safety enforcement
    - Tailwind CSS styling optimization
    - US Web Design System compliance
    - Section 508 accessibility validation
    - Zustand state management
    - TanStack Query integration
    - Performance optimization
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        logger.info("Frontend UX Agent initialized")
    
    def _get_prompt_template(self) -> str:
        """Get the prompt template for the frontend UX agent"""
        return """You are a Frontend UX Agent for the Fed Job Advisor system.

Your expertise includes:
- React component development with TypeScript
- Next.js 14 App Router patterns and best practices
- Tailwind CSS utility-first styling
- US Web Design System (USWDS) compliance
- Section 508 accessibility standards
- Zustand state management patterns
- TanStack Query for data fetching
- Performance optimization and bundle analysis
- Responsive design and mobile-first approach

CRITICAL CONSTRAINTS:
- Solo developer model: Simple, maintainable components over complex architectures
- Part-time development: Focus on reusable patterns and component libraries
- $0 budget: Use only free tools and public resources
- Accessibility first: All components must meet Section 508 standards
- Merit Hiring compliance: UI should support guidance tools, not content generation

TECHNOLOGY STACK:
- Next.js 14 with App Router
- React 18 with TypeScript
- Tailwind CSS with USWDS tokens
- Zustand for state management
- TanStack Query for server state
- Radix UI for accessible primitives
- React Hook Form for form handling

Available tools:
{tools}

Tool names: {tool_names}

When developing frontend features:
1. Always prioritize accessibility and usability
2. Follow USWDS design principles and patterns
3. Ensure TypeScript type safety
4. Optimize for performance and SEO
5. Create reusable, maintainable components
6. Test across different screen sizes

{agent_scratchpad}"""
    
    def _load_tools(self) -> List[Tool]:
        """Load tools specific to frontend development"""
        
        return [
            Tool(
                name="generate_react_component",
                func=self._generate_react_component,
                description="Generate a React component with TypeScript and Tailwind CSS"
            ),
            Tool(
                name="optimize_component_performance",
                func=self._optimize_component_performance,
                description="Analyze and optimize React component performance"
            ),
            Tool(
                name="validate_accessibility",
                func=self._validate_accessibility,
                description="Check component for Section 508 accessibility compliance"
            ),
            Tool(
                name="apply_uswds_patterns",
                func=self._apply_uswds_patterns,
                description="Apply US Web Design System patterns and styling"
            ),
            Tool(
                name="setup_state_management",
                func=self._setup_state_management,
                description="Configure Zustand store for component state management"
            ),
            Tool(
                name="implement_data_fetching",
                func=self._implement_data_fetching,
                description="Set up TanStack Query for data fetching and caching"
            ),
            Tool(
                name="optimize_bundle_size",
                func=self._optimize_bundle_size,
                description="Analyze and optimize component bundle size and loading"
            ),
            Tool(
                name="create_responsive_layout",
                func=self._create_responsive_layout,
                description="Create responsive layouts with Tailwind CSS breakpoints"
            )
        ]
    
    def _generate_react_component(self, specs: str) -> str:
        """Generate a React component based on specifications"""
        
        # Parse component specifications
        component_info = self._parse_component_specs(specs)
        
        component_code = f"""
// {component_info['name']}.tsx
import React from 'react';
import {{ clsx }} from 'clsx';

interface {component_info['name']}Props {{
  {component_info['props']}
  className?: string;
  children?: React.ReactNode;
}}

export const {component_info['name']}: React.FC<{component_info['name']}Props> = ({{
  {component_info['prop_destructuring']},
  className,
  children,
  ...props
}}) => {{
  return (
    <{component_info['element']}
      className={{clsx(
        '{component_info['base_classes']}',
        className
      )}}
      {{...props}}
    >
      {component_info['content']}
      {{children}}
    </{component_info['element']}>
  );
}};

export default {component_info['name']};
"""
        
        return f"""
Generated React Component: {component_info['name']}

Features:
- TypeScript interfaces for type safety
- Tailwind CSS styling with clsx utility
- Accessible markup structure
- Flexible props interface
- USWDS design tokens

Code:
{component_code.strip()}

Usage Example:
```tsx
import {{ {component_info['name']} }} from './components/{component_info['name']}';

<{component_info['name']} {component_info['example_props']}>
  Content here
</{component_info['name']}>
```

Next Steps:
1. Add unit tests with React Testing Library
2. Implement accessibility testing
3. Add Storybook documentation
4. Performance optimization review
"""
    
    def _optimize_component_performance(self, component: str) -> str:
        """Analyze and optimize component performance"""
        
        optimizations = []
        
        # Check for common performance issues
        if "useState" in component and "useEffect" in component:
            optimizations.append("Consider using useCallback for event handlers")
        
        if "map(" in component and "key=" not in component:
            optimizations.append("CRITICAL: Add unique keys to mapped elements")
        
        if "props." in component:
            optimizations.append("Consider destructuring props for cleaner code")
        
        if "inline function" in component.lower():
            optimizations.append("Move inline functions to useCallback")
        
        # Performance recommendations
        recommendations = [
            "Use React.memo() for pure components",
            "Implement lazy loading for heavy components",
            "Optimize image loading with next/image",
            "Use dynamic imports for code splitting",
            "Minimize bundle size with tree shaking"
        ]
        
        return f"""
Performance Analysis and Optimization

Issues Found:
{chr(10).join(f"- {opt}" for opt in optimizations) if optimizations else "- No critical issues detected"}

Optimization Strategies:
{chr(10).join(f"- {rec}" for rec in recommendations[:3])}

Performance Checklist:
□ Implement React.memo() where appropriate
□ Use useCallback for stable function references
□ Add unique keys to all list items
□ Optimize re-renders with useMemo
□ Implement lazy loading for route components
□ Bundle analysis with @next/bundle-analyzer

Code Example - Optimized Component:
```tsx
import React, {{ memo, useCallback, useMemo }} from 'react';

const OptimizedComponent = memo<Props>(({{ items, onItemClick }}) => {{
  const handleClick = useCallback((id: string) => {{
    onItemClick(id);
  }}, [onItemClick]);
  
  const sortedItems = useMemo(() => {{
    return items.sort((a, b) => a.name.localeCompare(b.name));
  }}, [items]);
  
  return (
    <ul>
      {{sortedItems.map(item => (
        <li key={{item.id}} onClick={{() => handleClick(item.id)}}>
          {{item.name}}
        </li>
      ))}}
    </ul>
  );
}});
```
"""
    
    def _validate_accessibility(self, component: str) -> str:
        """Validate component for accessibility compliance"""
        
        issues = []
        recommendations = []
        
        # Check for common accessibility issues
        if "onClick" in component and "onKeyDown" not in component:
            issues.append("CRITICAL: Interactive elements need keyboard support")
        
        if "<img" in component and "alt=" not in component:
            issues.append("CRITICAL: Images must have alt text")
        
        if "<button" in component and "aria-label" not in component and "aria-describedby" not in component:
            issues.append("WARNING: Buttons should have accessible labels")
        
        if "color-" in component and "contrast" not in component:
            issues.append("WARNING: Verify color contrast ratios")
        
        # Section 508 compliance recommendations
        recommendations = [
            "Use semantic HTML elements (header, nav, main, footer)",
            "Implement ARIA landmarks and labels",
            "Ensure 4.5:1 color contrast ratio minimum",
            "Support keyboard navigation patterns",
            "Add focus indicators for interactive elements",
            "Use heading hierarchy (h1, h2, h3, etc.)",
            "Provide alternative text for images",
            "Implement skip links for navigation"
        ]
        
        return f"""
Section 508 Accessibility Analysis

Issues Found:
{chr(10).join(f"- {issue}" for issue in issues) if issues else "- No critical accessibility issues detected"}

Compliance Checklist:
{chr(10).join(f"□ {rec}" for rec in recommendations)}

Accessible Component Pattern:
```tsx
import React, {{ useRef }} from 'react';

const AccessibleButton: React.FC<{{
  children: React.ReactNode;
  onClick: () => void;
  ariaLabel?: string;
  disabled?: boolean;
}}> = ({{ children, onClick, ariaLabel, disabled = false }}) => {{
  const buttonRef = useRef<HTMLButtonElement>(null);
  
  const handleKeyDown = (e: React.KeyboardEvent) => {{
    if (e.key === 'Enter' || e.key === ' ') {{
      e.preventDefault();
      onClick();
    }}
  }};
  
  return (
    <button
      ref={{buttonRef}}
      className="focus:ring-2 focus:ring-blue-500 focus:outline-none"
      onClick={{onClick}}
      onKeyDown={{handleKeyDown}}
      aria-label={{ariaLabel}}
      disabled={{disabled}}
      type="button"
    >
      {{children}}
    </button>
  );
}};
```

Testing Tools:
- axe-core for automated accessibility testing
- WAVE browser extension for manual testing
- Screen reader testing (NVDA, JAWS)
- Keyboard-only navigation testing
"""
    
    def _apply_uswds_patterns(self, component: str) -> str:
        """Apply US Web Design System patterns"""
        
        uswds_patterns = {
            "button": {
                "classes": "usa-button usa-button--primary",
                "variants": ["primary", "secondary", "accent-cool", "base"]
            },
            "form": {
                "classes": "usa-form usa-form--large",
                "components": ["input", "select", "textarea", "fieldset"]
            },
            "card": {
                "classes": "usa-card usa-card--header-first",
                "layout": ["header", "media", "body", "footer"]
            },
            "navigation": {
                "classes": "usa-nav usa-nav--primary",
                "patterns": ["header", "sidenav", "breadcrumb"]
            }
        }
        
        detected_pattern = "button"  # Default pattern
        for pattern in uswds_patterns.keys():
            if pattern.lower() in component.lower():
                detected_pattern = pattern
                break
        
        pattern_info = uswds_patterns[detected_pattern]
        
        return f"""
USWDS Pattern Application: {detected_pattern.title()}

Design System Classes:
- Base: {pattern_info['classes']}
- Responsive: usa-{detected_pattern}--mobile-lg
- Utility: margin, padding, color tokens

USWDS Component Structure:
```tsx
import React from 'react';
import clsx from 'clsx';

interface USWDSComponentProps {{
  variant?: '{pattern_info.get('variants', ['default'])[0]}' | 'secondary';
  size?: 'small' | 'default' | 'large';
  className?: string;
}}

export const USWDSComponent: React.FC<USWDSComponentProps> = ({{
  variant = '{pattern_info.get('variants', ['default'])[0]}',
  size = 'default',
  className,
  children
}}) => {{
  return (
    <div
      className={{clsx(
        '{pattern_info['classes']}',
        {{
          'usa-{detected_pattern}--secondary': variant === 'secondary',
          'usa-{detected_pattern}--small': size === 'small',
          'usa-{detected_pattern}--large': size === 'large',
        }},
        className
      )}}
    >
      {{children}}
    </div>
  );
}};
```

USWDS Design Tokens:
- Colors: usa-color('primary'), usa-color('base-darkest')
- Spacing: units(2), units(4), units(6)
- Typography: font-family('sans'), font-size('lg')
- Breakpoints: mobile, mobile-lg, tablet, desktop

Implementation Notes:
1. Import USWDS CSS in your layout
2. Configure Tailwind with USWDS tokens
3. Use semantic HTML structure
4. Follow USWDS accessibility guidelines
5. Test with government style guides
"""
    
    def _setup_state_management(self, state_specs: str) -> str:
        """Configure Zustand store for state management"""
        
        store_name = self._extract_store_name(state_specs)
        state_fields = self._extract_state_fields(state_specs)
        
        store_code = f"""
// stores/{store_name}Store.ts
import {{ create }} from 'zustand';
import {{ devtools, persist }} from 'zustand/middleware';

interface {store_name}State {{
  {state_fields['interface']}
}}

interface {store_name}Actions {{
  {state_fields['actions']}
}}

export const use{store_name}Store = create<{store_name}State & {store_name}Actions>()(
  devtools(
    persist(
      (set, get) => ({{
        // Initial state
        {state_fields['initial']}
        
        // Actions
        {state_fields['implementations']}
      }}),
      {{
        name: '{store_name.lower()}-storage',
        partialize: (state) => ({{ 
          // Only persist certain fields
          {state_fields['persist_fields']}
        }}),
      }}
    ),
    {{ name: '{store_name}Store' }}
  )
);

// Selectors for optimized re-renders
export const select{store_name}Data = (state: {store_name}State & {store_name}Actions) => state.data;
export const select{store_name}Loading = (state: {store_name}State & {store_name}Actions) => state.loading;
"""
        
        return f"""
Zustand Store Configuration: {store_name}

Features:
- TypeScript type safety
- Redux DevTools integration
- Persistence with localStorage
- Optimized selectors
- Middleware support

Store Implementation:
{store_code.strip()}

Usage in Components:
```tsx
import {{ use{store_name}Store, select{store_name}Data }} from './stores/{store_name}Store';

// Basic usage
const MyComponent = () => {{
  const {{ data, loading, fetchData }} = use{store_name}Store();
  
  return (
    <div>
      {{loading ? 'Loading...' : data.length}} items
      <button onClick={{fetchData}}>Refresh</button>
    </div>
  );
}};

// Optimized with selectors
const OptimizedComponent = () => {{
  const data = use{store_name}Store(select{store_name}Data);
  const loading = use{store_name}Store(select{store_name}Loading);
  
  // Component only re-renders when data or loading changes
  return <div>{{data.length}} items</div>;
}};
```

Best Practices:
- Use selectors to prevent unnecessary re-renders
- Keep stores focused and single-purpose
- Implement optimistic updates for better UX
- Use middleware for development tools
- Persist only essential state
"""
    
    def _implement_data_fetching(self, api_specs: str) -> str:
        """Set up TanStack Query for data fetching"""
        
        query_info = self._parse_api_specs(api_specs)
        
        query_code = f"""
// hooks/use{query_info['name']}.ts
import {{ useQuery, useMutation, useQueryClient }} from '@tanstack/react-query';
import {{ {query_info['name']}API }} from '@/lib/api';

// Query hook
export const use{query_info['name']} = ({query_info['params']}) => {{
  return useQuery({{
    queryKey: ['{query_info['key']}', {query_info['key_params']}],
    queryFn: () => {query_info['name']}API.get{query_info['name']}({query_info['api_params']}),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
    retry: 3,
    retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
    enabled: {query_info['enabled_condition']},
  }});
}};

// Mutation hook
export const useCreate{query_info['name']} = () => {{
  const queryClient = useQueryClient();
  
  return useMutation({{
    mutationFn: {query_info['name']}API.create{query_info['name']},
    onSuccess: () => {{
      // Invalidate and refetch
      queryClient.invalidateQueries({{ queryKey: ['{query_info['key']}'] }});
    }},
    onError: (error) => {{
      console.error('Failed to create {query_info['name'].lower()}:', error);
    }},
  }});
}};

// Prefetch hook for performance
export const usePrefetch{query_info['name']} = () => {{
  const queryClient = useQueryClient();
  
  return (params: {query_info['params']}) => {{
    queryClient.prefetchQuery({{
      queryKey: ['{query_info['key']}', params],
      queryFn: () => {query_info['name']}API.get{query_info['name']}(params),
      staleTime: 5 * 60 * 1000,
    }});
  }};
}};
"""
        
        return f"""
TanStack Query Data Fetching: {query_info['name']}

Features:
- Automatic caching and background updates
- Error handling and retry logic
- Optimistic updates
- Request deduplication
- Prefetching for performance

Implementation:
{query_code.strip()}

Component Usage:
```tsx
import {{ use{query_info['name']}, useCreate{query_info['name']} }} from '@/hooks/use{query_info['name']}';

const {query_info['name']}List = () => {{
  const {{ data, isLoading, error }} = use{query_info['name']}({{
    page: 1,
    limit: 10
  }});
  
  const create{query_info['name']}Mutation = useCreate{query_info['name']}();
  
  const handleCreate = async (formData: FormData) => {{
    try {{
      await create{query_info['name']}Mutation.mutateAsync(formData);
      // Success handled automatically by onSuccess
    }} catch (error) {{
      // Error handled automatically by onError
    }}
  }};
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {{error.message}}</div>;
  
  return (
    <div>
      {{data?.map(item => (
        <div key={{item.id}}>{{item.name}}</div>
      ))}}
    </div>
  );
}};
```

Query Client Setup:
```tsx
// app/providers.tsx
import {{ QueryClient, QueryClientProvider }} from '@tanstack/react-query';
import {{ ReactQueryDevtools }} from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({{
  defaultOptions: {{
    queries: {{
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
    }},
  }},
}});

export const Providers = ({{ children }}) => {{
  return (
    <QueryClientProvider client={{queryClient}}>
      {{children}}
      <ReactQueryDevtools initialIsOpen={{false}} />
    </QueryClientProvider>
  );
}};
```
"""
    
    def _optimize_bundle_size(self, component_path: str) -> str:
        """Analyze and optimize bundle size"""
        
        optimizations = [
            "Implement dynamic imports for route components",
            "Use tree shaking to eliminate unused code",
            "Optimize images with next/image component",
            "Split vendor bundles for better caching",
            "Implement code splitting at route level"
        ]
        
        return f"""
Bundle Size Optimization Analysis

Current Component: {component_path}

Optimization Strategies:
{chr(10).join(f"- {opt}" for opt in optimizations)}

Implementation Examples:

1. Dynamic Imports:
```tsx
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {{
  loading: () => <p>Loading...</p>,
  ssr: false, // Disable SSR if not needed
}});
```

2. Tree Shaking:
```tsx
// Instead of importing entire library
import {{ debounce }} from 'lodash';

// Import only what you need
import debounce from 'lodash/debounce';
```

3. Bundle Analyzer Setup:
```bash
npm install --save-dev @next/bundle-analyzer
```

```js
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({{
  enabled: process.env.ANALYZE === 'true',
}});

module.exports = withBundleAnalyzer({{}});
```

4. Code Splitting by Routes:
```tsx
// app/dashboard/page.tsx
import {{ lazy, Suspense }} from 'react';

const DashboardChart = lazy(() => import('./components/DashboardChart'));

export default function Dashboard() {{
  return (
    <Suspense fallback={{<div>Loading chart...</div>}}>
      <DashboardChart />
    </Suspense>
  );
}}
```

Performance Metrics to Track:
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- Bundle size per route
- Unused code percentage

Bundle Analysis Command:
```bash
ANALYZE=true npm run build
```

Optimization Checklist:
□ Remove unused dependencies
□ Implement lazy loading for heavy components
□ Use dynamic imports for route components
□ Optimize image loading and compression
□ Enable compression in production
□ Use CDN for static assets
"""
    
    def _create_responsive_layout(self, layout_specs: str) -> str:
        """Create responsive layouts with Tailwind CSS"""
        
        layout_info = self._parse_layout_specs(layout_specs)
        
        layout_code = f"""
// components/ResponsiveLayout.tsx
import React from 'react';
import {{ clsx }} from 'clsx';

interface ResponsiveLayoutProps {{
  children: React.ReactNode;
  sidebar?: React.ReactNode;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}}

export const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({{
  children,
  sidebar,
  header,
  footer,
  className
}}) => {{
  return (
    <div className={{clsx(
      'min-h-screen bg-gray-50',
      'grid grid-rows-[auto_1fr_auto]',
      'lg:grid-cols-[250px_1fr]',
      'lg:grid-rows-[auto_1fr_auto]',
      className
    )}}>
      {{/* Header */}}
      {{header && (
        <header className="lg:col-span-2 bg-white shadow-sm border-b">
          {{header}}
        </header>
      )}}
      
      {{/* Sidebar */}}
      {{sidebar && (
        <aside className={{clsx(
          'hidden lg:block lg:row-span-1',
          'bg-white border-r',
          'overflow-y-auto'
        )}}>
          {{sidebar}}
        </aside>
      )}}
      
      {{/* Main Content */}}
      <main className={{clsx(
        'flex-1 overflow-y-auto',
        'p-4 sm:p-6 lg:p-8',
        'max-w-full'
      )}}>
        <div className="max-w-7xl mx-auto">
          {{children}}
        </div>
      </main>
      
      {{/* Footer */}}
      {{footer && (
        <footer className="lg:col-span-2 bg-white border-t">
          {{footer}}
        </footer>
      )}}
    </div>
  );
}};

// Responsive Grid Component
export const ResponsiveGrid: React.FC<{{
  children: React.ReactNode;
  columns?: {{ sm?: number; md?: number; lg?: number; xl?: number }};
  gap?: number;
  className?: string;
}}> = ({{
  children,
  columns = {{ sm: 1, md: 2, lg: 3, xl: 4 }},
  gap = 6,
  className
}}) => {{
  const gridClasses = clsx(
    'grid',
    `gap-${{gap}}`,
    `grid-cols-${{columns.sm || 1}}`,
    `md:grid-cols-${{columns.md || 2}}`,
    `lg:grid-cols-${{columns.lg || 3}}`,
    `xl:grid-cols-${{columns.xl || 4}}`,
    className
  );
  
  return (
    <div className={{gridClasses}}>
      {{children}}
    </div>
  );
}};
"""
        
        return f"""
Responsive Layout Implementation: {layout_info['type']}

Tailwind CSS Breakpoints:
- sm: 640px and up
- md: 768px and up  
- lg: 1024px and up
- xl: 1280px and up
- 2xl: 1536px and up

Layout Code:
{layout_code.strip()}

Usage Examples:
```tsx
// Dashboard Layout
<ResponsiveLayout
  header={{<DashboardHeader />}}
  sidebar={{<DashboardSidebar />}}
  footer={{<DashboardFooter />}}
>
  <ResponsiveGrid columns={{{{ sm: 1, md: 2, lg: 3 }}}}>
    <DashboardCard />
    <DashboardCard />
    <DashboardCard />
  </ResponsiveGrid>
</ResponsiveLayout>

// Mobile-first Card Grid
<div className={{clsx(
  'grid gap-4',
  'grid-cols-1',           // Mobile: 1 column
  'sm:grid-cols-2',        // Small: 2 columns
  'md:grid-cols-3',        // Medium: 3 columns
  'lg:grid-cols-4',        // Large: 4 columns
  'xl:grid-cols-5'         // Extra large: 5 columns
)}}>
  {{items.map(item => <Card key={{item.id}} item={{item}} />)}}
</div>
```

Responsive Utilities:
- Container queries: @container queries for component-level responsiveness
- Aspect ratio: aspect-w-16 aspect-h-9 for consistent ratios
- Typography: responsive text sizing with text-sm md:text-base lg:text-lg
- Spacing: responsive padding/margins with p-4 md:p-6 lg:p-8

Mobile-First Best Practices:
1. Start with mobile styles (no prefix)
2. Progressive enhancement with breakpoint prefixes
3. Touch targets minimum 44px x 44px
4. Readable font sizes (minimum 16px)
5. Adequate contrast ratios
6. Test on real devices
"""
    
    def _parse_component_specs(self, specs: str) -> Dict[str, str]:
        """Parse component specifications"""
        return {
            "name": "CustomComponent",
            "element": "div",
            "props": "title: string;\n  onClick?: () => void;",
            "prop_destructuring": "title, onClick",
            "base_classes": "p-4 bg-white rounded-lg shadow",
            "content": "{title}",
            "example_props": 'title="Example" onClick={() => console.log("clicked")}'
        }
    
    def _extract_store_name(self, specs: str) -> str:
        """Extract store name from specifications"""
        if "job" in specs.lower():
            return "Job"
        elif "user" in specs.lower():
            return "User"
        else:
            return "App"
    
    def _extract_state_fields(self, specs: str) -> Dict[str, str]:
        """Extract state fields from specifications"""
        return {
            "interface": "data: any[];\n  loading: boolean;\n  error: string | null;",
            "actions": "fetchData: () => Promise<void>;\n  setData: (data: any[]) => void;\n  setLoading: (loading: boolean) => void;",
            "initial": "data: [],\n    loading: false,\n    error: null,",
            "implementations": "fetchData: async () => {\n      set({ loading: true, error: null });\n      try {\n        const data = await api.getData();\n        set({ data, loading: false });\n      } catch (error) {\n        set({ error: error.message, loading: false });\n      }\n    },\n    setData: (data) => set({ data }),\n    setLoading: (loading) => set({ loading }),",
            "persist_fields": "data: state.data"
        }
    
    def _parse_api_specs(self, specs: str) -> Dict[str, str]:
        """Parse API specifications"""
        return {
            "name": "Job",
            "key": "jobs",
            "params": "{ page: number; limit: number }",
            "key_params": "{ page, limit }",
            "api_params": "{ page, limit }",
            "enabled_condition": "!!page && !!limit"
        }
    
    def _parse_layout_specs(self, specs: str) -> Dict[str, str]:
        """Parse layout specifications"""
        return {
            "type": "dashboard" if "dashboard" in specs.lower() else "basic"
        }
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze frontend development request"""
        
        request = data.get("component_request", "")
        component_type = data.get("type", "component")
        context = data.get("context", {})
        
        if not request:
            return AgentResponse(
                success=False,
                message="No component request provided",
                data=None
            )
        
        try:
            response_data = {}
            
            if component_type == "component":
                response_data["component"] = self._generate_react_component(request)
                response_data["accessibility"] = self._validate_accessibility(request)
                response_data["uswds"] = self._apply_uswds_patterns(request)
            elif component_type == "performance":
                response_data["optimization"] = self._optimize_component_performance(request)
                response_data["bundle"] = self._optimize_bundle_size(request)
            elif component_type == "state":
                response_data["state_management"] = self._setup_state_management(request)
                response_data["data_fetching"] = self._implement_data_fetching(request)
            elif component_type == "layout":
                response_data["responsive_layout"] = self._create_responsive_layout(request)
            
            return AgentResponse(
                success=True,
                message="Frontend analysis completed",
                data=response_data,
                metadata={
                    "agent": "frontend_ux",
                    "type": component_type,
                    "request": request
                }
            )
        
        except Exception as e:
            logger.error(f"Frontend analysis failed: {e}")
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}",
                data=None
            )


# Export the agent class
__all__ = ["FrontendUXAgent"]