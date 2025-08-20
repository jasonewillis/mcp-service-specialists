"""
UX/Design Agent with shadcn/ui Integration
Specialized agent for creating modern, accessible UI components
"""

from typing import Dict, List, Any, Optional
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
import json

class UXDesignAgent:
    """UX/Design Agent specialized in shadcn/ui and modern React components"""
    
    def __init__(self, llm):
        self.llm = llm
        self.shadcn_components = self._load_shadcn_components()
        self.tools = self._create_tools()
        self.prompt = self._create_prompt()
    
    def _load_shadcn_components(self) -> Dict[str, Any]:
        """Load shadcn/ui component templates and patterns"""
        return {
            "accordion": {
                "description": "Collapsible content sections",
                "import": '@/components/ui/accordion',
                "usage": "FAQ sections, expandable lists, settings panels"
            },
            "alert-dialog": {
                "description": "Modal dialog for important actions",
                "import": '@/components/ui/alert-dialog',
                "usage": "Confirmations, warnings, critical actions"
            },
            "button": {
                "description": "Interactive button component",
                "import": '@/components/ui/button',
                "usage": "Actions, form submissions, navigation"
            },
            "card": {
                "description": "Container for grouped content",
                "import": '@/components/ui/card',
                "usage": "Content sections, feature highlights, data display"
            },
            "dialog": {
                "description": "Modal overlay for forms and content",
                "import": '@/components/ui/dialog',
                "usage": "Forms, detailed views, user input"
            },
            "dropdown-menu": {
                "description": "Menu with nested options",
                "import": '@/components/ui/dropdown-menu',
                "usage": "Navigation, actions, settings"
            },
            "form": {
                "description": "Form components with validation",
                "import": '@/components/ui/form',
                "usage": "User input, data collection, settings"
            },
            "input": {
                "description": "Text input field",
                "import": '@/components/ui/input',
                "usage": "Text entry, search, data input"
            },
            "select": {
                "description": "Dropdown selection component",
                "import": '@/components/ui/select',
                "usage": "Option selection, filters, settings"
            },
            "table": {
                "description": "Data table with sorting and filtering",
                "import": '@/components/ui/table',
                "usage": "Data display, lists, reports"
            },
            "tabs": {
                "description": "Tabbed content sections",
                "import": '@/components/ui/tabs',
                "usage": "Content organization, navigation, views"
            },
            "toast": {
                "description": "Notification messages",
                "import": '@/components/ui/toast',
                "usage": "Feedback, alerts, confirmations"
            }
        }
    
    def _create_tools(self) -> List[Tool]:
        """Create specialized tools for UX/Design tasks"""
        return [
            Tool(
                name="create_shadcn_component",
                func=self.create_shadcn_component,
                description="Create a shadcn/ui component with modern design"
            ),
            Tool(
                name="design_dashboard",
                func=self.design_dashboard,
                description="Design a complete dashboard layout"
            ),
            Tool(
                name="create_form",
                func=self.create_form,
                description="Create an accessible form with validation"
            ),
            Tool(
                name="design_mobile_responsive",
                func=self.design_mobile_responsive,
                description="Create mobile-responsive components"
            ),
            Tool(
                name="accessibility_audit",
                func=self.accessibility_audit,
                description="Audit component for accessibility"
            ),
            Tool(
                name="create_data_visualization",
                func=self.create_data_visualization,
                description="Design data visualization components"
            ),
            Tool(
                name="theme_customization",
                func=self.theme_customization,
                description="Create custom theme and color schemes"
            )
        ]
    
    def _create_prompt(self) -> PromptTemplate:
        """Create specialized prompt for UX/Design agent"""
        template = """You are a Senior UX/UI Designer specializing in modern React applications and shadcn/ui components.
        
        Your expertise includes:
        - Creating beautiful, accessible UI components using shadcn/ui
        - Implementing responsive design with Tailwind CSS
        - Following WCAG 2.1 accessibility guidelines
        - Designing intuitive user experiences
        - Creating consistent design systems
        
        Available shadcn/ui components:
        {shadcn_components}
        
        Design Principles:
        - Accessibility first (ARIA labels, keyboard navigation)
        - Mobile-responsive by default
        - Consistent spacing and typography
        - Dark mode support
        - Performance optimized
        
        Current task: {task}
        
        Provide a complete solution using shadcn/ui components and best practices.
        Include:
        1. Component imports
        2. Full implementation code
        3. Styling with Tailwind CSS
        4. Accessibility features
        5. Usage examples
        """
        
        return PromptTemplate(
            input_variables=["task", "shadcn_components"],
            template=template
        )
    
    def create_shadcn_component(self, component_request: str) -> str:
        """Create a shadcn/ui component based on requirements"""
        
        # Example: Create a job listing card for Fed Job Advisor
        if "job" in component_request.lower() or "card" in component_request.lower():
            return """
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MapPin, Briefcase, DollarSign, Shield } from "lucide-react"

interface JobCardProps {
  job: {
    id: string
    title: string
    agency: string
    series: string
    grade: string
    salary: {
      min: number
      max: number
    }
    location: string
    clearance?: string
    matchScore?: number
    postedDate: string
  }
  onApply?: (jobId: string) => void
  onSave?: (jobId: string) => void
}

export function JobCard({ job, onApply, onSave }: JobCardProps) {
  return (
    <Card className="w-full hover:shadow-lg transition-shadow duration-200">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <CardTitle className="text-xl font-semibold">
              {job.title}
            </CardTitle>
            <CardDescription className="text-sm text-muted-foreground">
              {job.agency}
            </CardDescription>
          </div>
          {job.matchScore && (
            <Badge variant="secondary" className="ml-2">
              {job.matchScore}% Match
            </Badge>
          )}
        </div>
        <div className="flex gap-2 mt-2">
          <Badge variant="outline">{job.series}</Badge>
          <Badge variant="outline">{job.grade}</Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-1">
            <MapPin className="h-4 w-4 text-muted-foreground" />
            <span>{job.location}</span>
          </div>
          {job.clearance && (
            <div className="flex items-center gap-1">
              <Shield className="h-4 w-4 text-muted-foreground" />
              <span>{job.clearance}</span>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-1 text-sm">
          <DollarSign className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium">
            ${job.salary.min.toLocaleString()} - ${job.salary.max.toLocaleString()}
          </span>
        </div>
        
        <p className="text-xs text-muted-foreground">
          Posted {job.postedDate}
        </p>
      </CardContent>
      
      <CardFooter className="flex gap-2">
        <Button 
          className="flex-1"
          onClick={() => onApply?.(job.id)}
        >
          Apply Now
        </Button>
        <Button 
          variant="outline"
          onClick={() => onSave?.(job.id)}
        >
          Save
        </Button>
      </CardFooter>
    </Card>
  )
}

// Usage Example:
// <JobCard 
//   job={{
//     id: "123",
//     title: "Data Scientist",
//     agency: "Department of Defense",
//     series: "1560",
//     grade: "GS-13",
//     salary: { min: 96970, max: 126062 },
//     location: "Washington, DC",
//     clearance: "Secret",
//     matchScore: 85,
//     postedDate: "2 days ago"
//   }}
//   onApply={(id) => console.log('Apply to job:', id)}
//   onSave={(id) => console.log('Save job:', id)}
// />
"""
        
        # Generate component based on request
        prompt = self.prompt.format(
            task=component_request,
            shadcn_components=json.dumps(self.shadcn_components, indent=2)
        )
        
        response = self.llm.generate(prompt)
        return response
    
    def design_dashboard(self, requirements: str) -> str:
        """Design a complete dashboard layout"""
        
        return """
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { BarChart, LineChart, Activity, Users, Briefcase, TrendingUp } from "lucide-react"

export function FederalJobDashboard() {
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-muted/10">
        <div className="p-6">
          <h2 className="text-lg font-semibold">Fed Job Advisor</h2>
        </div>
        <ScrollArea className="h-[calc(100vh-5rem)]">
          <nav className="space-y-2 p-4">
            <Button variant="ghost" className="w-full justify-start">
              <Briefcase className="mr-2 h-4 w-4" />
              Job Search
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <Activity className="mr-2 h-4 w-4" />
              My Applications
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <Users className="mr-2 h-4 w-4" />
              Profile
            </Button>
          </nav>
        </ScrollArea>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 overflow-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back! Here's your federal job search overview.</p>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Applications</CardTitle>
              <Briefcase className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-muted-foreground">+2 from last week</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Interview Requests</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs text-muted-foreground">Schedule available</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Match Score Avg</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">78%</div>
              <p className="text-xs text-muted-foreground">+5% improvement</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Saved Jobs</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">24</div>
              <p className="text-xs text-muted-foreground">8 closing soon</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Tabs */}
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="jobs">Job Matches</TabsTrigger>
            <TabsTrigger value="applications">Applications</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>
          
          <TabsContent value="overview" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Your job search activity from the past week</CardDescription>
              </CardHeader>
              <CardContent>
                {/* Activity content */}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
"""
    
    def create_form(self, form_type: str) -> str:
        """Create an accessible form with validation"""
        
        return """
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "@/components/ui/use-toast"

const formSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  grade: z.string().min(1, "Please select a grade"),
  series: z.string().min(1, "Please enter job series"),
  location: z.string().min(1, "Please select location"),
  clearance: z.string().optional(),
  experience: z.string().min(10, "Please describe your experience"),
})

export function FederalProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      grade: "",
      series: "",
      location: "",
      clearance: "",
      experience: "",
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    toast({
      title: "Profile Updated",
      description: "Your federal job profile has been saved successfully.",
    })
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Full Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormDescription>Your name as it appears on federal documents</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <FormField
          control={form.control}
          name="grade"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Current Grade</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your current grade" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="GS-5">GS-5</SelectItem>
                  <SelectItem value="GS-7">GS-7</SelectItem>
                  <SelectItem value="GS-9">GS-9</SelectItem>
                  <SelectItem value="GS-11">GS-11</SelectItem>
                  <SelectItem value="GS-12">GS-12</SelectItem>
                  <SelectItem value="GS-13">GS-13</SelectItem>
                  <SelectItem value="GS-14">GS-14</SelectItem>
                  <SelectItem value="GS-15">GS-15</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <Button type="submit" className="w-full">
          Save Profile
        </Button>
      </form>
    </Form>
  )
}
"""
    
    def design_mobile_responsive(self, component: str) -> str:
        """Create mobile-responsive component designs"""
        prompt = f"Create a mobile-responsive version of: {component}"
        return self.llm.generate(prompt)
    
    def accessibility_audit(self, component: str) -> str:
        """Audit component for accessibility issues"""
        return f"Accessibility audit for: {component}"
    
    def create_data_visualization(self, data_type: str) -> str:
        """Design data visualization components"""
        return f"Data visualization for: {data_type}"
    
    def theme_customization(self, requirements: str) -> str:
        """Create custom theme and color schemes"""
        return f"Theme customization for: {requirements}"