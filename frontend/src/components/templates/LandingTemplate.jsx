import HeroSection from '../organisms/HeroSection'
import SectionsGrid from '../organisms/SectionsGrid'
import WorkflowTimeline from '../organisms/WorkflowTimeline'
import NavigationBar from '../organisms/NavigationBar'
import WelcomeBanner from '../molecules/WelcomeBanner'

function LandingTemplate({ hero, sections, workflow }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Navigation Bar - Siempre visible */}
      <NavigationBar />
      
      {/* Welcome Banner - Solo cuando el usuario inicia sesión */}
      <WelcomeBanner />
      
      {/* Main Content - Con padding-top para no quedar debajo del navbar */}
      <div className="relative isolate overflow-hidden bg-grid px-6 pb-24 pt-24 sm:px-12">
        <div
          className="pointer-events-none absolute inset-x-0 top-0 h-72 bg-gradient-to-br from-brand-primary/30 via-brand-secondary/20 to-slate-900 blur-3xl"
          aria-hidden="true"
        />

        <div className="mx-auto flex max-w-6xl flex-col gap-12">
          <HeroSection {...hero} />
          <SectionsGrid sections={sections} />
          <WorkflowTimeline {...workflow} />
        </div>
      </div>
    </div>
  )
}

export default LandingTemplate
