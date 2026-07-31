export type Locale='zh'|'en';export type Phase='cover'|'incident'|'footage'|'report';export type EndingId='plug'|'maintenance'|'suite';
export interface Ending{id:EndingId;code:string;label:{zh:string;en:string};title:{zh:string;en:string};detail:{zh:string;en:string}}
