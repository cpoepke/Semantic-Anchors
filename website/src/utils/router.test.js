import { describe, it, expect, beforeEach, vi } from 'vitest'
import { addRoute, getCurrentRoute, initRouter, navigate } from './router.js'

describe('router', () => {
  beforeEach(() => {
    // Reset to base path
    history.replaceState(null, '', '/')
    window.location.hash = ''
  })

  it('returns current route from pathname', () => {
    history.replaceState(null, '', '/about')
    expect(getCurrentRoute()).toBe('/about')
  })

  it('supports legacy hash URLs for backward compatibility', () => {
    window.location.hash = '#/about'
    expect(getCurrentRoute()).toBe('/about')
  })

  it('navigates to a route via pushState', () => {
    navigate('/contributing')
    expect(window.location.pathname).toBe('/contributing')
  })

  it('runs registered handler on init and popstate', async () => {
    const handler = vi.fn()
    addRoute('/router-test', handler)
    history.replaceState(null, '', '/router-test')

    initRouter()
    expect(handler).toHaveBeenCalledTimes(1)

    history.pushState(null, '', '/router-test')
    window.dispatchEvent(new PopStateEvent('popstate'))
    expect(handler).toHaveBeenCalledTimes(2)
  })
})
