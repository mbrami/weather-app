import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

/*import {
   keepFresh,
    shareAndCache,
     retryExponentialBackoff
     } from 'http-operators';*/

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'testproject';
  repos;
  constructor(http: HttpClient) {
    const path = 'https://api.github.com/search/repositories?q=angular'
    this.repos = http.get<any>(path).pipe(
      map(result => result.items),
      /*keepFresh(100*1000)
      shareAndCache('github-angular-repos'),*/
    );
  }
}
