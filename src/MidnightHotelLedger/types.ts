export type Locale='zh'|'en';
export type Phase='cover'|'setup'|'incident'|'footage'|'report'|'complete';
export type SceneId='bath'|'checkin'|'bells';
export type OutcomeId='plug'|'maintenance'|'suite'|'passport'|'charge-eight'|'eight-signatures'|'unplug'|'eight-breakfasts'|'night-manager';
export type Copy={zh:string;en:string};
export interface Outcome{id:OutcomeId;label:Copy;title:Copy;detail:Copy;captions:{zh:string[];en:string[]};success:boolean;video:string;end:string}
export interface Scene{id:SceneId;caseNo:string;title:Copy;setup:Copy;question:Copy;alt:Copy;start:string;outcomes:Outcome[]}
